"""Build the profile pages from one content file per person.

    python profiles/_src/build.py            (run from the site root; Python 3.11+, no extra packages)

For every people/<slug>.toml it writes
    profiles/<slug>/index.html      the profile page (from template.html)
    <short_path>/index.html         a redirect to it, if the person has a short_path (from redirect.html)
and for every projects/<slug>.toml (a project's page, owned by `person`)
    profiles/<person>/projects/<slug>/index.html   (from project_page.html, a running system told in stages, or
                                                    study_page.html when kind = "study": a finished study told
                                                    as sections, with charts drawn by charts.py)

Site-wide settings (site name, base URL, visitor counter) are in site.toml.
Templates use a small Mustache subset:
    {{name}}            escaped text          {{{name}}}   raw HTML
    {{#name}}..{{/name}} section: repeats for a list, shows once for a true value, hides for empty/false
    {{^name}}..{{/name}} shown only when name is empty or false
    {{.}}               the current list item  a.b          dotted names
    {{> name}}          the contents of partials/name.html

All page content, headings and labels included, lives in people/<slug>.toml. Projects, publications
and talks each carry `order` (position) and `show` ("page" or "more", folded under "More ...").
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

import charts  # noqa: E402  (same folder)
import privacy_check  # noqa: E402  (same folder)


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


PARTIAL = re.compile(r"\{\{>\s*([\w-]+)\s*\}\}")


def expand_partials(template: str) -> str:
    """Replace {{> name}} with the contents of partials/name.html (partials may use partials)."""
    for _ in range(5):
        new = PARTIAL.sub(lambda m: (SRC / "partials" / f"{m.group(1)}.html").read_text(encoding="utf-8"), template)
        if new == template:
            return new
        template = new
    raise ValueError("template: partials nest too deeply")


def render(template: str, data: dict) -> str:
    return render_tree(parse(expand_partials(template)), [data])


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


# Lists whose entries carry `order` (position, ascending) and `show` ("page" = on the page,
# "more" = folded under the section's "More ..." toggle). The template uses <key>_page and <key>_more.
ORDERED_LISTS = ("projects", "publications", "talks")
# Card lists in two columns on wide screens: a phone shows only the first PHONE_CARDS of the cards on the page; the
# rest appear first under the section's "More ..." toggle there (Ibrahim, 24 Oct: 4 on desktop, 3 on phone).
PHONE_FOLDED = ("projects", "talks")
PHONE_CARDS = 3


def split_by_placement(slug: str, key: str, items: list) -> tuple[list, list]:
    for item in items:
        if not isinstance(item.get("order"), int) or item.get("show") not in ("page", "more"):
            raise SystemExit(f"{slug}: every [[{key}]] entry needs order = <number> and show = \"page\" or \"more\" "
                             f"(check '{item.get('title') or item.get('citation', '')[:40]}')")
    items = sorted(items, key=lambda i: i["order"])
    return [i for i in items if i["show"] == "page"], [i for i in items if i["show"] == "more"]


def check_private(slug: str, label: str, text: str, allowed: set[str]) -> None:
    problems = privacy_check.scan(text, allowed, label)
    if problems:
        raise SystemExit(f"{slug}: privacy check failed, nothing was written:\n  - " + "\n  - ".join(problems))


def whole_numbers(value):
    """Pages CMS writes every number as a float (order = 1.0); turn whole floats back into ints."""
    if isinstance(value, dict):
        return {k: whole_numbers(v) for k, v in value.items()}
    if isinstance(value, list):
        return [whole_numbers(v) for v in value]
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value


def build_person(site: dict, path: Path, template: str, redirect_template: str) -> list[Path]:
    raw = path.read_text(encoding="utf-8")
    p = whole_numbers(tomllib.loads(raw))
    slug = p["slug"]
    if path.stem != slug:
        raise SystemExit(f"{path.name}: slug '{slug}' must match the file name")
    allowed = privacy_check.allowed_emails(p)
    check_private(slug, path.name, raw, allowed)
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
    for key in ORDERED_LISTS:
        p[key + "_page"], p[key + "_more"] = split_by_placement(slug, key, p.get(key, []))
    for key in PHONE_FOLDED:
        extra = p[key + "_page"][PHONE_CARDS:]
        for item in extra:
            item["wide_only"] = True
        # the phone's copies, without the id (an id may appear only once on a page)
        p[key + "_phone_more"] = [{**{k: v for k, v in i.items() if k != "id"}, "wide_only": False, "narrow_only": True}
                                  for i in extra]
        p[key + "_fold_any"] = bool(extra or p[key + "_more"])
    for theme in p.get("themes", []):  # the Examples links, separated by " · " (none after the last)
        for n, example in enumerate(theme.get("examples", []), 1):
            example["last"] = n == len(theme["examples"])
    for group in p.get("skills", []):  # "R · Python · SQL" -> tags
        group["tags"] = [s.strip() for s in group.get("items", "").split("·") if s.strip()]
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
    page = render(template, data)
    check_private(slug, f"profiles/{slug}/index.html (page text)", privacy_check.page_text(page), allowed)
    out = page_dir / "index.html"
    out.write_text(page, encoding="utf-8", newline="\n")
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


# The boxes of a project page's system diagram (projects/<slug>.toml, [diagram]). Each label may use " | " to
# break its line; each has a <key>_stage, the stage card its number badge links to.
DIAGRAM_KEYS = ("sources", "rules", "ml", "screen", "evaluate", "human", "facts", "grades", "timing", "band")


def diagram_data(diagram: dict) -> dict:
    out = {}
    for key in DIAGRAM_KEYS:
        lines = [part.strip() for part in str(diagram.get(key, "")).split("|") if part.strip()]
        n = len(lines)
        out[key] = {
            "lines": [{"t": t, "dy": f"{-(n - 1) * 0.6:.1f}em" if i == 0 else "1.2em"} for i, t in enumerate(lines)],
            "one": " ".join(lines),
            "stage": diagram.get(key + "_stage", ""),
        }
    return out


def build_project(site: dict, path: Path, template: str) -> Path:
    """projects/<slug>.toml -> profiles/<person>/projects/<slug>/index.html (a project's "how it works" page)."""
    raw = path.read_text(encoding="utf-8")
    p = whole_numbers(tomllib.loads(raw))
    slug, owner = p["slug"], p["person"]
    if path.stem != slug:
        raise SystemExit(f"{path.name}: slug '{slug}' must match the file name")
    person = whole_numbers(tomllib.loads((SRC / "people" / f"{owner}.toml").read_text(encoding="utf-8")))
    allowed = privacy_check.allowed_emails(person)
    check_private(slug, path.name, raw, allowed)
    page_url = f"{site['base_url']}/profiles/{owner}/projects/{slug}/"

    updated = dt.date.fromisoformat(p["updated"]) if "updated" in p else dt.date.today()
    p["updated_iso"] = updated.isoformat()
    p["updated_human"] = f"{updated.day} {updated:%B %Y}"
    for i, stage in enumerate(p.get("stages", []), 1):
        stage["number"] = i
    # The closing boxes (Running underneath, Next, What I learned) show only when filled in.
    p["closing_any"] = bool(p.get("underneath") or p.get("next") or p.get("learned"))
    data = add_html_variants(p)
    if p.get("kind") == "study":
        template = (SRC / "study_page.html").read_text(encoding="utf-8")
        labels = p.get("labels", {})
        table_label = labels.get("data_table", "Data")
        daily = charts.read_daily(SRC / "projects" / p["daily_csv"]) if p.get("daily_csv") else []
        for sec in data.get("sections", []):
            chart = sec.get("chart")
            cap = sec.get("caption", "")
            if chart == "calendar":
                c = p["calendar"]
                sec["chart_html"] = charts.calendar(daily, cap, c["modes"], c["title"], c["description"], table_label)
            elif chart == "device":
                c = p["device"]
                sec["chart_html"] = charts.device_check(
                    daily, dt.date.fromisoformat(c["start"]), dt.date.fromisoformat(c["end"]),
                    dt.date.fromisoformat(c["marker"]), c["marker_label"], cap, c["title"], c["description"])
            elif chart == "phases":
                c = p["phases"]
                sec["chart_html"] = charts.phases(daily, dt.date.fromisoformat(c["start"]), dt.date.fromisoformat(c["end"]),
                                                  c["periods"], cap, c["title"], c["description"])
            elif chart == "effects":
                c = p["effects"]
                sec["chart_html"] = charts.effects(c["rows"], c["low"], c["high"], cap, table_label)
            elif chart == "picture":
                c = p["picture"]
                sec["chart_html"] = charts.picture_link(c["src"], c["alt"], c["href"], c["label"], cap, c["width"], c["height"])
            elif chart == "figure_set":
                sec["chart_html"] = charts.figure_set(sec["id"], sec["panels"], cap, p.get("figure_credit", ""),
                                                      sec.get("legend", "Tap to choose a chart"), sec.get("measures", []),
                                                      sec.get("grid") == "quad", p.get("tables", {}).get(sec["id"]))
            elif chart == "figures":
                sec["chart_html"] = charts.figures(sec["panels"], cap, p.get("figure_credit", ""))
            elif chart == "ladder":
                sec["chart_html"] = charts.ladder(p["ladder"], sec.get("caption", ""), labels.get("data_table", "Data"))
            elif chart == "recruit":
                sec["chart_html"] = charts.recruit(sec.get("caption", ""), p["recruit_title"], p["recruit_description"])
            elif chart == "flow":
                sec["chart_html"] = charts.flow(p["flow"], p["flow_title"], p["flow_description"])
            elif chart:
                raise SystemExit(f"{slug}: unknown chart '{chart}'")
    data.update(
        site=add_html_variants(site),
        page_url=page_url,
        person_name=person["name"],
        d=diagram_data(p.get("diagram", {})),
        aside_copy={"in_aside": True},
        analytics=site.get("analytics", {}).get("enabled") and site["analytics"].get("goatcounter_code"),
        goatcounter_code=site.get("analytics", {}).get("goatcounter_code", ""),
    )
    page = render(template, data)
    check_private(slug, f"profiles/{owner}/projects/{slug}/index.html (page text)", privacy_check.page_text(page), allowed)
    out_dir = PROFILES / owner / "projects" / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "index.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    return out


def main() -> int:
    site = tomllib.loads((SRC / "site.toml").read_text(encoding="utf-8"))
    site["base_url"] = site["base_url"].rstrip("/")
    template = (SRC / "template.html").read_text(encoding="utf-8")
    redirect_template = (SRC / "redirect.html").read_text(encoding="utf-8")
    project_template = (SRC / "project_page.html").read_text(encoding="utf-8")
    people = sorted((SRC / "people").glob("*.toml"))
    if not people:
        print("no content files in profiles/_src/people/")
        return 1
    for path in people:
        for out in build_person(site, path, template, redirect_template):
            print("wrote", out.relative_to(ROOT).as_posix())
    for path in sorted((SRC / "projects").glob("*.toml")):
        print("wrote", build_project(site, path, project_template).relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    sys.exit(main())
