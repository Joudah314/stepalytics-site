# Hand-over: Ibrahim Joudah profile page (stepalytics.com/profiles/ibrahim-joudah)

Updated 20 Oct 2026, end of session (5-hour limit 93% used). This file is for a session that continues the work. Read the task in "Task" first, then "What remains".

**Status:**
- **Done and saved:**
  - First complete version built: `site/profiles/ibrahim-joudah/index.html`.
  - One rubric check: `evaluation.md`, round 1, 83/100, gate passed, with a list of round-2 fixes.
  - Screenshots in `evaluation_shots/`.
- **Not yet done:**
  - Round 2 (apply the fixes listed in `evaluation.md`, rebuild, rescore).
  - Folding in `research/07` (brief), `research/09` and `research/10` (Sonnet follow-ups). These may still have been running when the session ended; each saves as it goes.
  - `content_map.md`. Every claim on the page comes from the kit.
- **Applied after the brief (`research/07`, complete):**
  - Removed the ROSE GitHub link: the repository is public but empty.
  - Removed "large language models and text embeddings" from Skills: that claim rests on the excluded survey project.
- **Issues found by the brief, for Ibrahim:**
  - Both Tableau dashboards open empty because their date filters default to today. They are linked as proof on the page.
  - CRAN's AirScreen page links the Logic314 account.
  - His Tableau Public headline says "Teacher / Educator".
  - The public CV's skills line still lists LLMs, NLP and text embeddings. Decide whether to drop them, as they rest on the excluded survey project.
  - The 2025 SSA NSW award (in the kit) could not be found online.

**Update, 20 Oct 2026 (later session):** round 2 is done and published. See `_notes/evaluation.md` (81 → 93/100, gate passed after six wording fixes from a claims check). `content_map.md` and folding in research/07, 09 and 10 were not redone; those files were not in the repository.

## Task (from Ibrahim, 20 Oct 2026)
Research what makes a professional profile page effective; turn it into a rubric; build his page as a static, local website ready for his GitHub Pages repository `stepalytics-site`. The page lives at `profiles/ibrahim-joudah/`, and `ibrahim-joudah/` redirects to it.

Rules:
- Read-only on everything except this folder. Publish, upload, push and account creation are not allowed.
- The kit (`C:\Users\ibrah\Documents\GitHub\Job-hunt\application_kit\`) is the source of truth. Obey `do_not_claim.md` exactly.
- Public or published work only. Leave out the 2026 consumer-survey project.
- Contact on the page is limited to the industry email, LinkedIn and the city (Sydney). Never a phone number, address, visa or work-rights details, grades, or the job-alerts mailbox.
- Subagents run on Sonnet or Opus, never Fable.

Final summary Ibrahim wants: the research's main findings; rubric scores before and after; what was removed from the public CV; defaults and open questions; claims from outside the kit; how to add a person; the exact publishing steps. Then open the page in his browser.

## Done
- **Research:**
  - `research/01`–`06`: Opus subagents, stopped early, each with a source log and a "Hand-over" section.
  - `research/08`: stepalytics.com look, complete.
  - Merged into `research_notes.md` (findings with grades, plus the design decisions in §8).
- **Rubric:** `rubric.md`. 13 weighted criteria totalling 100, plus a pass/fail gate for accuracy and privacy.
- **Public CV:**
  - In `cv_public/`. `make_public_cv.py` makes the public source from a verbatim copy of the kit CV; `check_pdf_private.py` scans the PDF.
  - What was removed is listed in `cv_public/REMOVED.md`. The output is `site/profiles/ibrahim-joudah/Ibrahim-Joudah-CV.pdf`, checked page by page.
- **Generator** (`site/profiles/_src/`):
  - `build.py`: Python 3.11+, no extra packages.
  - `template.html`, `redirect.html`, `site.toml` (visitor counter off), `people/ibrahim-joudah.toml` (the one content file), and `make_photo.py` (Pillow).
- **Page:** `site/profiles/ibrahim-joudah/` holds `index.html` (generated), `photo-*.webp/jpg`, `og-image.jpg` and the CV. `site/profiles/assets/` holds `profile.css` and `stepalytics-logo.png`. `site/ibrahim-joudah/index.html` is the redirect.

## What remains
1. **Fold in the Sonnet follow-ups.**
   - Sources: `research/09_followup_hiring_elements.md` and `research/10_followup_practical_reading.md`.
   - Fold them into `research_notes.md` (append a "Follow-ups" section). Adjust `rubric.md` only if they change a criterion.
2. **Fold in the brief.** `research/07_about_ibrahim_brief.md` (subagent 7) may hold facts to check:
   - the public status of the ROSE repository;
   - what the StepAlytics "program" was;
   - any personal interests.
   Correct the content file if it conflicts with the kit.
3. **Evaluate.**
   - Write `evaluation.md`: score the page against `rubric.md` at 375 × 812 and 1280 × 800 (rounds: first version, then after fixes).
   - Fix the weakest criteria, rebuild, and score again (at least two rounds).
4. **Write `content_map.md`.** List every claim on the page with its kit source (statement IDs S-xxx, `profile.md`, the CV) and mark claims from outside the kit. All claims come from the kit except the links listed under "Outside the kit".
5. **Give Ibrahim the final summary** (see "Task"), then open `site/profiles/ibrahim-joudah/index.html` in his browser.

## Decisions taken
| Question | Decision | Why |
|---|---|---|
| One page or several | One page with an "On this page" list; `<details>` only for optional depth | research_notes §4, §8 |
| Headline | "Data Scientist, Statistician & Applied AI Specialist" | The kit's headline on all CVs (preferences.md C14); role noun first |
| First screen | Photo, name, headline, value line, 4 proof cards, Email / LinkedIn / CV buttons, visible email address | rubric criterion 1 |
| Call to action | Email (primary), LinkedIn, CV; repeated in Contact; no form | research_notes §5 |
| Personal side | One line: StepAlytics began with his own tracker data; Arabic and English | kit S-186, S-094 |
| Testimonial | One 2024 student-evaluation comment (kit S-082), attributed as such | kit-approved, real |
| Left out | The 2026 survey project; job-hunt system (not public); work rights (S-191); iRTP scholarship on the page (its name implies student status; it stays in the CV) | Ibrahim's rules |
| Look | stepalytics.com tokens; system fonts; light theme only (the site has no dark mode); link teal `#017A7B` for contrast | research/08 |
| Redirect | Folder `ibrahim-joudah/index.html`: 0-second meta refresh, JS `location.replace`, absolute canonical, noindex. A one-hop alternative is `ibrahim-joudah.html`; never use both | research/06, research/08 |
| Counter | GoatCounter in `site.toml`, off (`enabled = false`) | research/06 |
| Video | Template slot `[video]` in the content file renders only if present; nothing shown now | Ibrahim |
| Public CV location line | Header location removed; institution and conference cities kept | Default; see `cv_public/REMOVED.md` |

## Files
- `research/`: subagent files (01–06 research, 07 brief, 08 look, 09–10 Sonnet follow-ups)
- `research_notes.md`: merged findings and decisions
- `rubric.md`: weighted criteria
- `cv_public/`: CV source copy, public source, builds, checks, `REMOVED.md`
- `site/`: copy its contents into the repository root. `profiles/_src` (underscore) is not published by Jekyll.

## Build, add a person, publish
- **Build:** `python profiles/_src/build.py` (run from `site/`). It rebuilds every page, refuses content with phone numbers, visa or work-rights words, or grades, and checks that the photo, CV and preview image exist.
- **Add a person:**
  1. Copy `profiles/_src/people/ibrahim-joudah.toml` to `<slug>.toml` and edit it.
  2. Run `python profiles/_src/make_photo.py <photo.jpg> <slug>` and add `og-image.jpg` and a CV PDF to `profiles/<slug>/` (or remove `[cv]`).
  3. Build.
- **Publish:**
  1. Copy the contents of `site/` into the root of a local clone of `Joudah314/stepalytics-site`.
  2. Check `git status`: only `profiles/` and `ibrahim-joudah/` should be new, and no `.md` file sits outside `_src`.
  3. Commit with LF line endings and push.
  4. After Pages rebuilds, check https://stepalytics.com/ibrahim-joudah and the page.
  5. Optionally submit the page in Google Search Console, and turn on GoatCounter in `site.toml`, then rebuild.

**Update, 20 Oct 2026 (Ibrahim's requests):**
- **CV:** the site CV is now the industry CV (kit `cv_industry/`, 3 pages), built with TeX Live 2023 after removing the blank lines inside each rubric (they add rows in this curve version). Removed for the public copy:
  - the phone number;
  - the work-rights sentence;
  - the MRes mark and the GPA;
  - the referees (other people's emails).
  Ibrahim asked (20 Oct 2026) for the consumer-survey project and the LLM, NLP and text-embedding skills to stay in the public CV, so they are kept.
  The scrubbed source is not kept in this public repository.
- **First-screen boxes,** in industry order: PhD in Statistics (passed examination, Oct 2026), 2 live dashboards, R package on CRAN, 6 papers.
- **Photo:** the white-shirt photo, framed with a small margin above the hair, the tops of the shoulders showing and the head about two-thirds of the height (the top 50 px of soft ceiling is extended upward). The background was softened with a GrabCut mask and a background-only blur. `og-image.jpg` was updated to match.

**Update, 20 Oct 2026 (agentic AI project, round 3):**
- The project "Agentic AI job-market monitoring system" (kit D77, S-192 to S-194) is the first card. Selected work shows four cards (`[[projects]]`); the rest are in `[[more_projects]]`, folded. Cards take an optional `id`, `did_label` and a `how` list ("How it works").
- The folded publications list (`[[other_pubs]]`) holds only the papers not featured.
- The CV was rebuilt from the updated industry CV with the same removals. Building it with TeX Live 2023 (curve v1.16) needs `\vspace{-\baselineskip}` after lists, added through enumitem `after=` in a scratch copy, so it keeps 3 pages.
- Scores: `_notes/evaluation.md`, round 3 (85 → 94).
- **Ibrahim's answers to the round-3 proposals (20 Oct 2026):**
  - Dashboards: he will fix the Tableau date filters himself, so the box stays.
  - Folding the EPA role and the 2019 internship under "Earlier roles": no.
  - Removing the 2017 and 2018 KFUPM student prizes: no.
  - Do not propose either again.
  - A public artefact for the agentic AI system: he is considering it.
- **Public pages show what the agentic AI system does and how well, never how it works (Ibrahim, 21 Oct 2026).** The card, Skills and the public CV entry use only the public wording in the kit, S-195 (statements.md, marked "public: website and public CV only"). Never add detail beyond S-195 on any public page or in the public CV.
- **Thursday 22 Oct:** a short "Project overview" page (not a case study) at `profiles/ibrahim-joudah/agentic-ai/`, linked from the card as "Project overview". It covers what the system does, the results and scale numbers he approves, and how its trustworthiness was checked. At most a three-box diagram (Collect → Evaluate → Notify), with no internals, step order, thresholds, prompts, sources or methods. Presented as complete. Show him screenshots before pushing.
