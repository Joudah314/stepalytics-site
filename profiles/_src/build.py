"""Build the profile pages from one content file per person.

    python profiles/_src/build.py            (run from the site root; Python 3.11+, no extra packages)

For every people/<slug>.toml it writes
    profiles/<slug>/index.html      the profile page (from template.html)
    <short_path>/index.html         a redirect to it, if the person has a short_path (from redirect.html)

Site-wide settings (site name, base URL, visitor counter) are in site.toml.
Templates use a small Mustache subset:
    {{name}}            escaped text          {{{name}}}   raw HTML
    {{#name}}..{{/name}} section: repeats for a list, shows once for a true value, hides for empty/false
    {{^name}}..{{/name}} shown only when name is empty or false
    {{.}}               the current list item  a.b          dotted names
Every text field x also has x_html: the text with **bold**, *italic*, `code` and [links](url).
"""
from __future__ import annotations

import datetime as dt
import html
import json
import re
import sys
import tomllib
from pathlib import Path

SRC = Path(__file__).resolve().parent          # profiles/_src
PROFILES = SRC.parent                          # profiles
ROOT = PROFILES.parent                         # site root

# A content file must never carry these (the page is public). Extend as needed.
PRIVATE_PATTERNS = [
    (r"\+61[\s\d]{6,}|\b04\d{2}[\s]?\d{3}[\s]?\d{3}\b", "an Australian phone number"),
    (r"\b(visa|subclass\s*\d{3}|work(ing)? rights|permanent resident)\b", "visa or work-rights details"),
    (r"\b(GPA|WAM)\b|\b\d{2}/100\b", "a grade"),
]


# ---------------------------------------------------------------- text helpers
def inline_md(text: str) -> str:
    """Escape text, then apply **bold**, *italic*, `code` and [label](url)."""
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out)

    def link(m: re.Match) -> str:
        label, url = m.group(1), html.unescape(m.group(2))
        if not re.match(r"^(https://|http://|mailto:|#|\.{0,2}/|[\w-]+\.(pdf|html)$)", url):
            raise ValueError(f"unexpected link target: {url}")
        return f'<a href="{html.escape(url)}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, out)


def add_html_variants(value):
    """Give every string field x a sibling x_html (inline markdown rendered), and every
    list field x the siblings x_any (non-empty?) and x_count. Strings inside lists
    become {text, text_html}."""
    if isinstance(value, dict):
        out = {}
        for k, v in value.items():
            out[k] = add_html_variants(v)
            if isinstance(v, str):
                out[k + "_html"] = inline_md(v)
            elif isinstance(v, list):
                out[k + "_any"] = bool(v)
                out[k + "_count"] = len(v)
        return out
    if isinstance(value, list):
        return [{"text": v, "text_html": inline_md(v)} if isinstance(v, str) else add_html_variants(v)
                for v in value]
    return value


# ---------------------------------------------------------------- mini Mustache
TAG = re.compile(r"\{\{\{\s*([\w.]+)\s*\}\}\}|\{\{\s*([#^/!]?)\s*([^}]*?)\s*\}\}")


def parse(template: str):
    """Turn a template into a tree of strings and tag tuples."""
    root: list = []
    stack = [("", root)]
    pos = 0
    for m in TAG.finditer(template):
        stack[-1][1].append(template[pos:m.start()])
        pos = m.end()
        if m.group(1):
            stack[-1][1].append(("raw", m.group(1)))
            continue
        kind, name = m.group(2), m.group(3)
        if kind == "!":
            continue
        if kind in "#^" and kind:
            node = ("section" if kind == "#" else "inverted", name, [])
            stack[-1][1].append(node)
            stack.append((name, node[2]))
        elif kind == "/":
            if stack[-1][0] != name:
                raise ValueError(f"template: {{{{/{name}}}}} closes {{{{#{stack[-1][0]}}}}}")
            stack.pop()
        else:
            stack[-1][1].append(("var", name))
    if len(stack) != 1:
        raise ValueError(f"template: unclosed section {stack[-1][0]}")
    root.append(template[pos:])
    return root


def lookup(name: str, ctx: list):
    if name == ".":
        return ctx[-1]
    first, *rest = name.split(".")
    for frame in reversed(ctx):
        if isinstance(frame, dict) and first in frame:
            value = frame[first]
            for part in rest:
                value = value.get(part) if isinstance(value, dict) else None
            return value
    return None


def render_tree(tree, ctx: list) -> str:
    out = []
    for node in tree:
        if isinstance(node, str):
            out.append(node)
            continue
        kind, name = node[0], node[1]
        value = lookup(name, ctx)
        if kind == "var":
            out.append("" if value is None else html.escape(str(value)))
        elif kind == "raw":
            out.append("" if value is None else str(value))
        elif kind == "section":
            if isinstance(value, list):
                for item in value:
                    out.append(render_tree(node[2], ctx + [item]))
            elif value:
                out.append(render_tree(node[2], ctx + [value]))
        elif kind == "inverted":
            if not value:
                out.append(render_tree(node[2], ctx))
    return "".join(out)


def render(template: str, data: dict) -> str:
    return render_tree(parse(template), [data])


# ---------------------------------------------------------------- page data
def file_size_label(path: Path) -> str:
    kb = path.stat().st_size / 1024
    return f"{kb:,.0f} KB" if kb < 1024 else f"{kb / 1024:.1f} MB"


def jsonld(site: dict, p: dict, page_url: str) -> str:
    person = {
        "@type": "Person",
        "@id": page_url + "#person",
        "name": p["name"],
        "url": page_url,
        "jobTitle": p["headline"],
        "description": p["summary_plain"],
        "image": page_url + p["photo"]["fallback"],
    }
    sd = p.get("structured_data", {})
    if p.get("contact", {}).get("email"):
        person["email"] = "mailto:" + p["contact"]["email"]
    if sd.get("same_as"):
        person["sameAs"] = sd["same_as"]
    if sd.get("knows_about"):
        person["knowsAbout"] = sd["knows_about"]
    if sd.get("knows_language"):
        person["knowsLanguage"] = sd["knows_language"]
    if sd.get("alumni_of"):
        person["alumniOf"] = [{"@type": "CollegeOrUniversity", "name": n} for n in sd["alumni_of"]]
    if sd.get("works_for"):
        person["worksFor"] = [{"@type": "Organization", "name": n} for n in sd["works_for"]]
    if sd.get("home_location"):
        person["homeLocation"] = {"@type": "Place", "name": sd["home_location"]}
    page = {
        "@context": "https://schema.org",
        "@type": "ProfilePage",
        "@id": page_url,
        "url": page_url,
        "name": f"{p['name']} – {p['headline']}",
        "inLanguage": site.get("language", "en"),
        "dateModified": p["updated_iso"],
        "isPartOf": {"@type": "WebSite", "name": site["site_name"], "url": site["base_url"] + "/"},
        "mainEntity": person,
    }
    text = json.dumps(page, ensure_ascii=False, indent=2)
    return text.replace("</", "<\\/")


def check_private(slug: str, raw_text: str) -> None:
    for pattern, what in PRIVATE_PATTERNS:
        m = re.search(pattern, raw_text, flags=re.I)
        if m:
            raise SystemExit(f"{slug}: content file seems to contain {what}: '{m.group(0)}'")


def build_person(site: dict, path: Path, template: str, redirect_template: str) -> list[Path]:
    raw = path.read_text(encoding="utf-8")
    p = tomllib.loads(raw)
    slug = p["slug"]
    if path.stem != slug:
        raise SystemExit(f"{path.name}: slug '{slug}' must match the file name")
    check_private(slug, raw)
    page_dir = PROFILES / slug
    page_url = f"{site['base_url']}/profiles/{slug}/"

    needed = [p["photo"]["fallback"]] + re.findall(r"([\w.-]+\.\w+)\s+\d+w", p["photo"].get("webp_srcset", ""))
    if p.get("og_image"):
        needed.append(p["og_image"]["file"])
    for rel in needed:
        if not (page_dir / rel).is_file():
            raise SystemExit(f"{slug}: file missing: profiles/{slug}/{rel}")
    cv = p.get("cv")
    if cv:
        cv_path = page_dir / cv["file"]
        if not cv_path.is_file():
            raise SystemExit(f"{slug}: CV file missing: profiles/{slug}/{cv['file']}")
        cv["size"] = file_size_label(cv_path)

    updated = dt.date.fromisoformat(p["updated"]) if "updated" in p else dt.date.today()
    p["updated_iso"] = updated.isoformat()
    p["updated_human"] = f"{updated.day} {updated:%B %Y}"
    titles = [m["title"][:1].lower() + m["title"][1:] for m in p.get("more_projects", [])]
    p["more_projects_titles"] = ", ".join(titles[:-1]) + " and " + titles[-1] if len(titles) > 1 else "".join(titles)
    p["summary_plain"] = re.sub(r"\[([^\]]+)\]\([^)]+\)|[*`]", lambda m: m.group(1) or "", p["summary"])

    data = add_html_variants(p)
    data.update(
        site=add_html_variants(site),
        page_url=page_url,
        jsonld=jsonld(site, p, page_url),
        year=updated.year,
        analytics=site.get("analytics", {}).get("enabled") and site["analytics"].get("goatcounter_code"),
        goatcounter_code=site.get("analytics", {}).get("goatcounter_code", ""),
    )
    written = []
    out = page_dir / "index.html"
    out.write_text(render(template, data), encoding="utf-8", newline="\n")
    written.append(out)

    short = p.get("short_path")
    if short:
        short_dir = ROOT / short
        short_dir.mkdir(parents=True, exist_ok=True)
        data["target_relative"] = "../" * len(Path(short).parts) + f"profiles/{slug}/"
        out = short_dir / "index.html"
        out.write_text(render(redirect_template, data), encoding="utf-8", newline="\n")
        written.append(out)
    return written


def main() -> int:
    site = tomllib.loads((SRC / "site.toml").read_text(encoding="utf-8"))
    site["base_url"] = site["base_url"].rstrip("/")
    template = (SRC / "template.html").read_text(encoding="utf-8")
    redirect_template = (SRC / "redirect.html").read_text(encoding="utf-8")
    people = sorted((SRC / "people").glob("*.toml"))
    if not people:
        print("no content files in profiles/_src/people/")
        return 1
    for path in people:
        for out in build_person(site, path, template, redirect_template):
            print("wrote", out.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
