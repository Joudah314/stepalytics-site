# Research notes: what makes a professional profile page effective

Merged 20 Oct 2026 from the subagent files in `research/`. References such as [01-S4] point to file 01, source S4, where the full citation and numbers are logged.
Grades: **A** strong (peer-reviewed experiment, field study or meta-analysis, large survey with clear methods; or a standard or official documentation, for how-it-works facts); **B** moderate (rigorous usability research, small or dated peer-reviewed studies, large industry surveys with stated methods); **C** weak (vendor or industry data with unclear methods, small samples); **D** opinion.

How complete this is:
- Files 01–06 were stopped early at Ibrahim's request (usage limit). Each holds a source log of 18–39 sources plus a hand-over (main findings, sources trusted less, open searches).
- File 07 (brief about Ibrahim) and file 08 (stepalytics.com look) are separate.
- Sonnet follow-ups ran the open searches. Their results are in files 09–10 and are folded in at the end of this note.

## 1. Attention: what screeners look at, and for how long

- **The "6 seconds" figure is vendor data (C).**
  - TheLadders' 6 s (2012) and 7.4 s (2018) cover only the first fit/no-fit pass, with no disclosed method or statistics [01-S1–S3].
  - With little time pressure, a one-page CV gets about 14–16 s, read top-down and then re-checked for experience and education (B) [01-S5][01-S6].
- **Longer looks at experience predict advancing (A/B).** The largest recruiter eye-tracking study (221 recruiters, 2,043 CV views) found that longer viewing, and longer dwell on Experience in particular, predicted a candidate advancing; skimming went with rejection [01-S4].
- **The first screen gets most of the attention (B).**
  - 57% of viewing time is above the fold and 74% in the first two screenfuls (NN/g, 2018, desktop) [01-S17][04-S7].
  - Half of page visits last under 12 s, and 76% of clicks land in the initially visible area [04-S6].
- **Reviewers often don't click (A).** 58% of employers opened a linked CV, and 23% expanded any "learn more" section [01-S8]. So key facts must sit on the page itself, not behind links or toggles.
- **Technical evaluators skim cheap, verifiable signals (B).** They look first at recency, owned versus forked projects, accepted contributions and project reputation: an overview, then the personal site, then detail only if it is one click away. Inactivity eliminates [01-S13][01-S25][01-S26].
- **Formal beats creative (B).** Formal layouts beat creative ones with the same content, roughly doubling the interview chance. Bullets, bold titles, aligned dates and specific claims are preferred [01-S22][01-S23].
- **Volume is high (B/C).** Applications per ad are at record levels in Australia (2026), and more than 90% of employers filter with an ATS [01-S18–S20].

## 2. What data science hiring managers value

- **Communication is demanded as much as technique (B).**
  - In 198 healthcare data-scientist ads, storytelling and actionable results appeared in about 67% and communicating findings in about 59%, beside statistics at about 70% [02-S9].
  - Communication is in the UK's top 10 advert skills [02-S7].
  - Organisations name business knowledge and communication among the top missing skills [02-S6].
- **Good work is problem-first (B).** It is tied to a decision, sceptical of the data, validated and statistically rigorous [02-S1][02-S12].
- **Public work corroborates the CV rather than replacing it (C).**
  - 81% of managers screen the CV first [02-S4].
  - 70% of employers research candidates online, mostly to confirm qualifications [02-S18].
  - Recruiters look candidates up, and what they find changes callbacks (A) [05-S2][05-S12].
- **Costly, verified signals beat vanity metrics (B).** Reviewers trust owned projects, merged contributions and third-party verification, and distrust stars, forks and followers [02-S2][02-S17].
- **Narrative and reproducibility set work apart because the norm is poor (A).** 27.6% of public notebooks have no text at all, and only 4% reproduce [02-S10][02-S11].
- **Credentials rank low (C/B).** Certificates and degree prestige count for little; independent projects are seen as at least as convincing as academic achievements [02-S4][02-S5][02-S7].
- **PhDs are valued but met with reservations (A/B, C).**
  - Australian supervisors rate research graduates highly once hired; collaboration is their weakest domain (A/B) [02-S14].
  - Employer reservations are business savvy, teamwork and communication (C) [02-S13].
  - So the page should show applied, collaborative, stakeholder-facing evidence next to the research.

## 3. First impressions and credibility

- **Appeal is judged fast and sticks (B/A).**
  - Appeal is judged within 50–500 ms and barely changes with longer viewing (page means r = .92–.98) [03-S1–S4].
  - Low visual complexity and high prototypicality ("looks like what this kind of page should look like") win, with effects already visible at 17 ms. Complexity matters more than colour. Viewers over 45, and PhD holders, penalise busy pages more (A) [03-S4][03-S5].
- **Design is a gate; content earns trust (B).** 94% of rejection comments were about design, and 83% of comments on chosen sites were about content [03-S13]. Experts rely on cited sources and depth (B/C) [03-S9][03-S10].
- **Specific factors move credibility (B).**
  - Negative: rarely updated content (−1.67), broken links (−1.45), hard navigation (−1.30) and typos (−1.28).
  - Positive: easy contact (+1.5 to +2.0), credentials and citations (+1.49) and links to outside sources (+1.25).
  - Source: [03-S8][03-S11][03-S14].
- **Personal websites give fairly accurate impressions (A).** Impressions agree with the person's actual personality (mean r = .42), and rich, specific content helps [03-S17][03-S18].
- **Faces are judged within 100 ms (A/B).** A slight smile beats a broad one for perceived competence, better clothing raises perceived competence, and real photos get looked at while stock photos are ignored [03-S19–S23][03-S15].
- **Profile completeness helps (A, abstract only).** On online profiles, length, a photo and connections raise hiring recommendations; skill lists and endorsements barely matter [03-S21][01-S10][01-S11].

## 4. How people read; one page or several

- **Structure for scanners (B).**
  - Descriptive, distinct headings allow efficient "layer-cake" scanning, while walls of text produce F-pattern misses [04-S1–S4].
  - Readers take in about the first two words (11 characters) of list items, so headings, bullets and links should be front-loaded [04-S24].
  - Concise, scannable and objective text gave +124% measured usability (B, small n) [04-S9]. Needless long words lower perceived intelligence (B) [04-S26], and experts want plain text too (C) [04-S25].
- **Typography (A, desktop).**
  - Body text around 18 px, near-default line spacing [04-S10].
  - About 50–75 characters per line [04-S11].
  - On phones, comprehension of ordinary text equals desktop (B) [04-S12].
- **Progressive disclosure (B to D).**
  - Hide only optional depth [04-S13–S15]. Horizontal tabs are often overlooked.
  - Native `<details>` is found by find-in-page and opened by fragment links in current Chrome, Firefox and WebKit (A) [04-S23]. Screen readers announce it inconsistently, and there should be no headings or links inside `<summary>` (B) [06-S29–S31].
- **One page or several (B/D).**
  - Don't split linear content [04-S21][04-S22].
  - Paging helps for studying complex text (B) [04-S18][04-S19].
  - For a profile: one scrolling overview page, with depth in `<details>` or on linked pages.
  - An "On this page" list near the top shows the page's scope (C) [04-S17].

## 5. Specific elements

- **Photo: include one modest, high-quality headshot on the page; none on the PDF CV.**
  - Photos shift callbacks in both directions, and their weight falls when other evidence is strong (A) [05-S1][05-S2][05-S18].
  - Australian norm: no photo on CVs, a photo on profile pages (D) [05-S11].
  - Australian audits show large penalties for Arabic and Middle Eastern names (A) [05-S3][05-S4]. So lead with individuating evidence: specific achievements, publications and live work.
- **Headline:** front-load a searchable role noun, since readers take in about two words (B) [05-S23][04-S24].
- **Summary:** 50–100 factual words; heavy self-promotion is penalised (B) [05-S19–S21].
- **Quantified results:** concrete wording is judged truer (A, indirect) [05-S16]. Precision signals knowledge, but spurious precision backfires with experts (B) [05-S17]. Quantify only what is real and sourced.
- **Testimonials:** only named, specific ones. Favourable references erased a callback gap (A, formal letters) [05-S5].
- **Personal side:** one short line, after the professional evidence, showing initiative or contribution. Leave out class, religious and political markers; they swing callbacks either way (A/B) [05-S12–S15].
- **Call to action:**
  - One primary action: a visible email address (mailto link plus copyable text) in the first screen, repeated at the bottom. LinkedIn is secondary. No contact form (B for placement; D for form versus email) [05].
  - Easy contact raises credibility [03-S11].
- **CV PDF:** offered as a document to forward or print, labelled with type, pages, size and date (B/C) [05-S24].

## 6. Practical quality

- **Mobile:** in September 2026, Australian page views were 48.6% mobile and 48.5% desktop (B) [06-S36]. There are no primary data on which devices recruiters use.
- **Speed (A):**
  - Core Web Vitals "good" thresholds are LCP ≤ 2.5 s, INP ≤ 200 ms and CLS ≤ 0.1 [06-S12].
  - Budget: ≤ 200 KB and ≤ 10 requests, with no third parties (the median mobile home page is about 2.5 MB) [06-S22][06-S23].
  - Fonts: use system fonts. Google Fonts no longer gains from a shared cache, sends visitor IPs to Google and fails offline [06-S17–S19].
  - Images: width and height on every `img`; the hero image not lazy-loaded, with high fetch priority; WebP with a JPEG fallback [06-S20][06-S21][06-S24].
- **Accessibility (A):**
  - WebAIM Million 2026: 95.9% of home pages fail. The top failures are low contrast (83.9%), missing alt text (53.1%), empty links (46.3%) and a missing page language (13.5%) [06-S25].
  - New in WCAG 2.2 AA: 2.4.11 Focus Not Obscured, and 2.5.8 Target Size, at least 24 × 24 CSS px [06-S26][06-S28].
- **Name search and sharing (A):**
  - ProfilePage with Person as `mainEntity` is valid structured data [06-S1][06-S2]. It requires a name; recommended properties are description, image, sameAs and dateModified. Expect no visible rich result.
  - Title, h1 and og:title should match, with the name first [06-S3][06-S8].
  - Link previews need og:title, og:description, og:url and an og:image of at least 1200 × 627, as JPG or PNG [06-S9–S11].
- **Redirects (A):**
  - Google treats a 0-second meta refresh as a permanent redirect [06-S4][06-S5]. GitHub Pages 301s `/folder` to `/folder/` [06-S6][06-S7].
  - Use an absolute canonical URL with a trailing slash.
- **Visitor counting:** GoatCounter sets no cookies and stores no IPs [06-S39]. Load its script from an `https://` URL, not a protocol-relative `//` one.
- **Dark mode:** the site has none. A light theme matches stepalytics.com; if dark mode is added, both themes must pass contrast (A/B) [06-S34][06-S35].

## 7. The stepalytics.com look (file 08)

- **Build:** a hand-written static site on GitHub Pages, built by the default Jekyll 3.10 with no config.
  - HTML without front matter is copied unchanged, and folders starting with `_` are not published.
  - Any `.md` file in the repository would become a public page.
- **Brand:**
  - Colours: navy `#012150`, teal `#018182` (use `#017A7B` for text: 4.80:1), gold `#C7922C` (accent only; it fails as text), slate `#5B6770`, background `#F5F7F9`, text `#333`.
  - Cards are white with a 2 px `#DCE3E8` border and square corners; panels are `#E6EFEF` with an 8 px radius; no shadows.
  - Font: the system stack ("Segoe UI", system-ui, …). Content width 1040 px.
- **Voice:** plain, exact and sentence case, with middle dots, no marketing words and en-AU conventions.
- **Integration:** `/profiles/` and `/ibrahim-joudah/` are both free. Shared logo and favicon are at `/assets/`. No header, nav or footer exists to update.

## 8. Decisions taken from the research

| Question | Decision | Main evidence |
|---|---|---|
| One page or several | One scrolling page with an "On this page" list; optional depth (full publication list, talks, details of each role) in `<details>`; key facts always visible | §1, §4 |
| Headline title | "Data Scientist, Statistician & Applied AI Specialist": the kit's headline on all three CVs (C14), front-loading the searchable role noun | §5; kit preferences.md |
| First screen | Name, title, a value line, 3–4 verifiable proof points, email address and mailto, LinkedIn, CV PDF, photo | §1, §3, §5 |
| Call to action | "Email me" as the primary action, with the address visible; LinkedIn and the CV secondary; repeated at the bottom; no form | §5 |
| Projects | 3–4 cards framed problem → approach → result, each with a labelled link to the public artefact | §2 |
| Personal side | One short line after the evidence: StepAlytics began with a year of his own step-tracker data, and his languages | §5 |
| Testimonials | One short, real student-evaluation comment from the kit (S-082), attributed as such; no invented or unattributed quotes | §5 |
| Look | stepalytics.com tokens, system fonts, white cards with square corners, no shadows, light theme | §3, §7 |

## 9. Follow-ups (Sonnet, research/09, complete: 16 sources)
- GitHub and portfolios are used to corroborate the CV; curated work counts, not volume (B). HackerRank's "84.1%" is not on the report page; don't rely on it.
- PhDs: no data-science study found. A systematic review (B) says employers worry about teamwork and application, not rigour. This supports showing collaborative and applied work, as the page does.
- Titles: ABS OSCA 2024 separates Data Scientist (223234, builds and deploys ML) from Statistician (223133, study design). No counts of ad titles were found. Carrying both nouns, as the headline does, is right.
- Third-party, specific signals weigh more than self-description (A/B); specific testimonials beat generic praise (Pallais 2014, A). This supports linking artefacts and the attributed student comment.
- Plain language aids understanding and credibility, and jargon hurts even when defined (A/B). This raises the priority of round-2 fix 1 in `evaluation.md` (simplify the approach lines).
- Typos: 2 errors cut interview probability by about 7 points, 5 errors by about 18 (A, n = 445). A spell-check of the built page is required before publishing (round-2 fix 5).
- No experiment on quantified bullets; competency statements help (B). Captions help video; video is optional and low priority (B).
- These findings confirm the rubric; no weights change. research/10 (practical and reading) was still running when this was written.
