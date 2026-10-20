# Evaluation rubric: a profile page for industry data science hiring managers

Decided on 20 Oct 2026 from `research_notes.md`, before any design work. References such as [01-S4] point to the research files.

**Scoring.** Each criterion is scored 0–4:
- 0: absent
- 1: poor
- 2: partial
- 3: good
- 4: excellent, meeting every check listed

Weighted score = Σ weight × score / 4, out of 100.

**Gate (pass/fail, before scoring).** The page fails outright if any of these is true:
- a claim contradicts the application kit or `do_not_claim.md`;
- it uses non-public work or results;
- it shows a phone number, street address, visa or work-rights details, grades, or the job-alerts mailbox.

| # | Criterion | Weight | Evidence (grade) | How to judge (all at 375 × 812 and 1280 × 800) |
|---|---|---|---|---|
| 1 | **First screen answers "who, what, why you, how to reach"** | 12 | First viewport gets 57%, and the first two screens 74%, of viewing time; half of visits last < 12 s (B) [01-S17][04-S6][04-S7]; first pass is a quick fit check (C) [01-S1] | In the first screen: name, role title, one value line, 3–4 proof points, a visible email address, LinkedIn, CV link, photo. 4 = all present at both widths; 3 = one missing on phone; 2 = two or more missing |
| 2 | **Clear, searchable headline** | 5 | Readers take in about 2 words (B) [04-S24][05-S23]; recruiters pattern-match titles (C) [05-S10] | Starts with a recognised role noun matching his target roles; identical in title, h1, og:title, CV and LinkedIn; no slogan |
| 3 | **Specific, quantified, honest claims** | 10 | Concrete wording is judged truer (A, indirect) [05-S16]; spurious precision backfires (B) [05-S17]; experience dwell predicts advancing (A/B) [01-S4] | Each role or project states a concrete outcome; numbers only where real and sourced; no adjectives standing in for evidence ("passionate", "expert") |
| 4 | **Projects framed problem → approach → result** | 12 | Practitioners value problem-first, decision-tied, validated work (B) [02-S1][02-S12]; narrative and reproducibility set work apart (A) [02-S10][02-S11]; evaluators want owned, recent work (B) [01-S13][01-S25] | 3–4 featured projects on real problems, each with problem, approach, result and tools, and a public artefact; at least one applied/industry-facing example; recency visible |
| 5 | **Verifiable links one click away, clearly labelled** | 8 | Costly, verified signals are trusted (B) [02-S2][02-S17]; citations and outside links raise credibility (B) [03-S11]; many reviewers don't click (A) [01-S8] | Every artefact claim (paper, package, dashboard, repo) links to it; link text names the destination; the PDF link gives type, pages, size and date; no broken links; key facts are stated on the page, not only behind links |
| 6 | **Plain, concise communication** | 9 | Concise, scannable, objective text: +124% usability (B) [04-S9]; communication is demanded as much as technique (B) [02-S9]; needless long words lower perceived intelligence (B) [04-S26] | Summary 50–100 words; every featured paper has a one-line plain-English "why it matters"; jargon explained or avoided; no buzzwords; first person, active voice |
| 7 | **Scannable structure; depth on demand** | 9 | Descriptive headings allow layer-cake scanning (B) [04-S1–S4]; front-load text (B) [04-S24]; hide only optional depth (B–D) [04-S13–S15]; `<details>` works with find-in-page (A) [04-S23] | One page; descriptive headings; ≤ 4 bullets per item; an "On this page" list; `<details>` only for optional depth; nothing essential hidden; no headings or links inside `<summary>` |
| 8 | **Professional, credible look that matches stepalytics.com** | 9 | Low complexity and prototypicality win within 17–50 ms (A) [03-S4][03-S5]; design is the gate (B) [03-S13]; typos, outdated content and broken links hurt (B) [03-S8]; formal beats creative (B) [01-S22] | Uses the site's colours and type; restrained (one accent colour, no decoration); aligned grid; no typos; "Updated" date visible; consistent date formats |
| 9 | **One clear call to action** | 7 | Easy contact: +1.5 to +2.0 credibility (B) [03-S11]; one primary action, visible email, no form (B/D) [05]; PDF labelling (B/C) [05-S24] | Primary "Email me" with the address visible in the first screen and at the end; LinkedIn and CV secondary; contact block repeated at the bottom; no form |
| 10 | **Human element, used carefully** | 4 | Faces judged within 100 ms; slight smile and smart clothes help (A) [03-S19–S23]; personal sites give accurate impressions (A) [03-S17]; hobbies can swing callbacks either way (A/B) [05-S12–S15]; named references help (A) [05-S5] | One good headshot with useful alt text; one short personal line after the evidence, with no class, religious or political markers; testimonials only if real and attributed |
| 11 | **Accessibility (WCAG 2.2 AA)** | 7 | Top failures are contrast, alt text, empty links and missing lang (A) [06-S25]; 2.4.11 and 2.5.8 (A) [06-S26][06-S28] | Text contrast ≥ 4.5:1 (UI ≥ 3:1); alt text; `lang`; landmarks and heading order; skip link; visible focus not hidden by sticky elements; targets ≥ 24 px; reflow at 320 px; no information by colour alone |
| 12 | **Fast, mobile-first, works offline** | 4 | CWV thresholds; ≤ 200 KB, ≤ 10 requests (A) [06-S12][06-S22]; system fonts (A/B) [06-S17]; ~49% of Australian views on mobile (B) [06-S36]; 18 px body, 50–75 characters per line (A) [04-S10][04-S11] | Page weight ≤ 200 KB excluding the CV; ≤ 10 requests; no third-party requests; image sizes set (CLS 0); body ≥ 16 px; line length ≤ 75 characters; opens from disk with nothing missing |
| 13 | **Findable by name, previews well** | 4 | ProfilePage + Person (A) [06-S1][06-S2]; title, h1 and og consistent (A) [06-S3]; og:image ≥ 1200 × 627 (A/B) [06-S9]; 0-second redirect = permanent (A) [06-S4] | `<title>` and h1 start with the name; meta description; absolute canonical URL; valid JSON-LD (ProfilePage, Person, sameAs); Open Graph and Twitter tags with a 1200 × 630 image; short URL redirects in one step to the canonical URL |

Total weight: 100.

## Out of scope for scoring

Video. A slot exists in the template but is off, and nothing about video is shown.
