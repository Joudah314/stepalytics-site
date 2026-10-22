"""Privacy check for the profile pages: nothing private may be published.

    python profiles/_src/privacy_check.py        (run from the site root, after build.py)

Checks every people/<slug>.toml and every built page (profiles/<slug>/index.html and its
short-link redirect) for: a phone number, a street address, grades, visa or work-rights
details, and any email address other than the person's contact email (so no university
email). Exits with status 1 and says what was found, and where, without repeating the
private text itself (the GitHub Actions log of a public repository is public).
build.py runs the same check before it writes anything.
"""
from __future__ import annotations

import html
import re
import sys
import tomllib
from pathlib import Path

SRC = Path(__file__).resolve().parent          # profiles/_src
ROOT = SRC.parent.parent                       # site root

# (rule, pattern, flags). Patterns aim at the real thing, not at look-alikes such as DOIs,
# ORCIDs, page ranges or years.
RULES = [
    ("a phone number", r"\+\d{1,3}[\s.-]?\(?\d[\d\s().-]{6,}\d", 0),
    ("a phone number", r"\b04\d{2}[\s.-]?\d{3}[\s.-]?\d{3}\b", 0),
    ("a phone number", r"\(0[2378]\)\s?\d{4}[\s.-]?\d{4}\b", 0),
    ("a phone number", r"\b0[2378][\s.-]\d{4}[\s.-]?\d{4}\b", 0),
    ("a phone number", r"\b1[38]00[\s.-]?\d{3}[\s.-]?\d{3}\b", 0),
    ("a street address", r"\b\d{1,5}[A-Za-z]?(?:/\d{1,5})?\s+(?:[A-Z][a-z']+\s+){1,3}"
                         r"(?:Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|Ln|Place|Pl|Court|Ct|Crescent|Cres|"
                         r"Parade|Pde|Highway|Hwy|Boulevard|Blvd|Terrace|Tce|Way|Close|Circuit|Cct|Square|Sq)\b", 0),
    ("a street address", r"\b(?:Unit|Apartment|Apt|Suite)\s+\d+", re.I),
    ("a street address", r"\bP\.?\s?O\.?\s+Box\s+\d+", re.I),
    ("a street address", r"\b(?:NSW|VIC|QLD|SA|WA|TAS|ACT|NT)\s+\d{4}\b", 0),
    ("a grade", r"\b(?:GPA|WAM|ATAR)\b", 0),
    ("a grade", r"\bgrade point\b|\bfinal mark\b|\bhigh distinction\b|\bdistinction average\b|\bcredit average\b", re.I),
    ("a grade", r"\b\d{1,3}(?:\.\d+)?\s?/\s?100\b", 0),
    ("a grade", r"\b[0-4]\.\d{1,2}\s?/\s?(?:4|7)(?:\.0+)?\b", 0),
    ("visa or work-rights details", r"\bvisas?\b|\bsubclass\s*\d{3}\b|\bwork(?:ing)?[\s-]+rights\b|\bright[\s-]+to[\s-]+work\b"
                                    r"|\bpermanent[\s-]+residen\w*|\bcitizenship\b|\bsponsorship\b|\bbridging\b|\bwork permit\b", re.I),
]
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def allowed_emails(person: dict) -> set[str]:
    email = (person.get("contact") or {}).get("email", "")
    return {email.lower()} if email else set()


def scan(text: str, allowed: set[str], where: str) -> list[str]:
    """Return one message per finding: the rule broken and the line, never the text itself."""
    problems = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rule, pattern, flags in RULES:
            if re.search(pattern, line, flags):
                problems.append(f"{where}, line {lineno}: looks like {rule}")
        for email in EMAIL.findall(line):
            if email.lower() not in allowed:
                kind = "a university email" if re.search(r"\.(?:edu|ac)(?:\.[a-z]{2})?$", email.lower()) else "an email address"
                problems.append(f"{where}, line {lineno}: {kind} other than the contact email")
    return problems


def page_text(page_html: str) -> str:
    """The text a visitor can see or find in the page source, one block per line."""
    text = re.sub(r"<script\b.*?</script>", "", page_html, flags=re.S | re.I)
    text = re.sub(r"<(?:/p|/li|/h\d|/dd|/dt|br|/div|/summary)\b[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r'href="mailto:([^"]+)"', r" \1 ", text)
    return html.unescape(re.sub(r"<[^>]+>", " ", text))


def check_all() -> list[str]:
    problems = []
    for toml_path in sorted((SRC / "people").glob("*.toml")):
        raw = toml_path.read_text(encoding="utf-8")
        person = tomllib.loads(raw)
        allowed = allowed_emails(person)
        problems += scan(raw, allowed, toml_path.relative_to(ROOT).as_posix())
        built = [ROOT / "profiles" / person["slug"] / "index.html"]
        if person.get("short_path"):
            built.append(ROOT / person["short_path"] / "index.html")
        for page in built:
            if page.is_file():
                problems += scan(page_text(page.read_text(encoding="utf-8")), allowed,
                                 page.relative_to(ROOT).as_posix() + " (page text)")
    return problems


def main() -> int:
    problems = check_all()
    if problems:
        print("Privacy check FAILED: nothing was published. Remove the following, then save again:")
        for p in problems:
            print("  - " + p)
            print(f"::error title=Privacy check::{p}")      # shown on the GitHub Actions run page
        return 1
    print("Privacy check passed: no phone number, street address, grades, visa or work-rights details, "
          "or email other than the contact email.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
