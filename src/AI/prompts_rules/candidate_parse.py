CV_EXTRACTOR_RULES = """
Extract all information present in the provided text into a
CandidateProfile JSON object, following the schema exactly.

────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────

Extract, never invent.

The text is the single source of truth. Every field you populate must
be directly traceable to something explicitly stated in the text.

If a piece of information is not present, leave the corresponding field
as null, an empty string, or an empty array/list, as appropriate to the
schema. Never guess, infer beyond what is stated, or fill gaps with
plausible-sounding content.

────────────────────────────────────────
EXTRACTION RULES
────────────────────────────────────────

Personal information:
- Extract name, email, phone, and location exactly as written.
- Extract website, github, or linkedin if explicitly present as a URL or
  handle in the text.
- Do not extract or infer a professional title/role here — Personal has
  no such field. A target role, if needed, comes from the job offer, not
  from the candidate's own text.

Summary:
- If the text contains a professional summary, objective, or profile section,
  extract it exactly as written.
- If no summary exists in the text, leave this field as an empty string.
- Do NOT generate or write a summary. Extract only what exists.

Experience:
- Extract each job/role as a separate entry.
- Preserve company names, job titles, and dates exactly as written.
- Do not merge two roles into one entry, even if they are at the same company.
- Do not split one continuous role into multiple entries.
- Extract each distinct accomplishment as one Achievement object with these
  fields:
  * context: any explicitly stated situation, constraint, or problem the
    bullet(s) describe. If the text gives no context beyond the action
    itself, leave this as an empty string — do not invent a backstory.
  * action: the concrete action/responsibility as described in the text.
    This is the only field that must always be filled from the bullet.
  * impact: any explicitly stated outcome, result, or reason/purpose, in
    the candidate's own words. Leave empty string if the text states none.
  * metric: only fill this if the text gives an actual measurable figure
    (e.g., "150 MB saved", "5 ms frame time"). Populate `value` with the
    figure and `context_note` with whatever surrounding detail the text
    gives about it (hardware, scale, dataset, etc.). If the text gives a
    number with no surrounding context at all, still extract it as
    `value` and leave `context_note` as an empty string — do not invent
    context that isn't there. If there is no figure, leave `metric` as
    null entirely.
  * keywords: leave as an empty list. Keyword tagging is not part of
    extraction.
  Default to one bullet = one Achievement. However, when two or more
  CONSECUTIVE bullets in the source clearly describe the same underlying
  initiative from different angles (e.g., one bullet states the technical
  decision/action, and the very next bullet states the reason, constraint,
  or performance goal behind that same decision — such as "Implemented X
  using Y" followed by "Designed so that X supports Z under heavy load"),
  merge them into a SINGLE Achievement: put the decision/action in `action`,
  and put the reason/constraint/goal bullet in `context` or `impact` as
  appropriate (context if it explains a prior constraint, impact if it
  explains the resulting benefit). Do not merge bullets that describe
  clearly separate accomplishments just because they are adjacent — only
  merge when one bullet is materially about the same initiative as the
  other, not merely on a related topic.
  Never rewrite, paraphrase, or embellish the source wording when filling
  these fields — reuse the text's own phrasing, only redistributing it
  across context/action/impact/metric (across one bullet, or across the
  small number of consecutive bullets you've identified as one initiative).
- Company field:
  * Extract the real employer/organization name exactly as written.
  * If the text does not name a real company (e.g. it only says "Volunteer",
    "Independent", "Solo", "Personal project", or gives no employer at all),
    do NOT put that word in `company` as if it were an organization name.
    Leave `company` as an empty string instead, and instead reflect the
    unpaid/independent nature of the work through `is_professional = false`
    (see below) — `company` must only ever contain an actual employer name
    or be empty, never a status label.
- For dates, populate a DateRange as MM/YYYY for both start and end:
  * If the text gives a full month and year for a given side of the range
    (start or end), use it directly (e.g. "March 2022" -> "03/2022").
  * If the text gives only a single year for the WHOLE experience (e.g.
    "2023" as the only date, meaning the person worked there during that
    calendar year, with no other start/end given), treat it as spanning
    that entire year: start = "01/<year>", end = "12/<year>". Do NOT set
    start and end to the same month — that would misrepresent a full
    year of work as a single day.
  * If the text gives only a year on ONE side of an otherwise-dated range
    (e.g. "2021 - March 2023"), use "01/<year>" only for that one side,
    keeping the other side's real month/year as given — never touch the
    side that already has a specific month.
  * If "Present", "Actualidad", or "Presente" is used for the end date,
    extract it as-is (do not convert it to a date).
  * If a date is missing entirely, do not fabricate one — flag the
    experience by leaving that side of the range as an empty string only
    if the schema allows it; otherwise skip fields you cannot support
    with a real value rather than guessing.
- Set is_professional to true unless the text explicitly indicates the
  work was unpaid, volunteer, or a personal/solo project kept in the
  experience section (e.g., "unpaid", "indie, no salary", "solo work").

Education:
- Extract institution, degree, and field exactly as written.
- If the degree name includes the field (e.g., "Higher National Diploma -
  Web Application Development"), extract the field separately as
  "Web Application Development".
- Extract achievements/highlights as an array of plain strings if present,
  exactly as described in the text (Education achievements are strings,
  not Achievement objects — do not force them into context/action/impact).
- Education has no date fields in this schema — do not attempt to extract
  or place dates here, even if the text mentions them elsewhere.

Skills (CRITICAL - NO DUPLICATES):
- Each skill must appear in EXACTLY ONE category:
  * skills: Technical knowledge, software, tools, programming languages,
    frameworks, engines, libraries, methodologies, hard skills. Each item
    is a Skill object with `name` (required), `abbreviation` (optional),
    and `category` (optional free-text label like "Engines", "Languages").
  * soft_skills: Personal attributes, work style, behavioral traits
    (e.g., "Independent", "Team player", "Problem solver") — plain strings.
  * transferable_skills: Domain-specific practical abilities applicable
    across industries (e.g., "Dog Training", "Creative Writing",
    "Customer Service") — plain strings.
- Extract each technology, tool, or programming language as an individual
  Skill object, never grouped into a single string.
- Use canonical names when the source uses an obvious variant:
  "C++17/20" -> name "C++", "Python 3" -> name "Python".
- When the text gives both a full name and an abbreviation for the same
  technical skill (e.g., "Single Instruction, Multiple Data (SIMD)",
  "Structure of Arrays (SoA)"), split them: `name` gets the full term,
  `abbreviation` gets the short form. Do not merge them back into one
  string like "SIMD (Single Instruction, Multiple Data)".
- If the text gives only an abbreviation with no full name spelled out,
  put the abbreviation in `name` and leave `abbreviation` null — do not
  invent the expansion yourself.
- If a skill could fit multiple categories, choose the MOST SPECIFIC one.
  Example: "Team Leadership" -> soft_skills, NOT skills.
  Example: "Dog Training" -> transferable_skills, NOT skills.
- NEVER duplicate the same skill across multiple categories.

Projects:
- Extract personal, unpaid, or side projects described as such.
- For each project, extract:
  * name: The project name.
  * achievements: an array of Achievement objects (same structure and
    same rules as in Experience above — context/action/impact/metric),
    one per specific accomplishment, feature, or technical detail
    described in the text. Projects have no separate summary/description
    field — any brief overview the text gives should be folded into the
    `context` or `action` of the relevant achievement instead of being
    stored anywhere else.
  * technologies: an array of Skill objects (same rules as the Skills
    section above) for technologies, tools, or languages used in the
    project.
  * date: a DateRange if start/end dates are present in the text
    (same date rules as Experience above); otherwise omit it.
- Do NOT move projects into paid experience.

Languages:
- Only extract spoken/written languages here, never programming languages
  or tools.
- Extract proficiency level only if explicitly stated.
- Format: {"language": "English", "level": "Fluent"}

Additional information:
- Extract any other relevant information not covered above (volunteer work,
  certifications, hobbies, interests) as an array of strings.

────────────────────────────────────────
WHAT YOU MUST NOT DO
────────────────────────────────────────

Never:
- Invent employers, titles, dates, or degrees not present in the text.
- Infer a skill from context alone (e.g., do not add "Leadership" just
  because someone "managed a team" unless the text uses that or an
  equivalent explicit term).
- Invent a metric, a context, or an impact that the text does not state —
  leave those Achievement fields empty rather than filling them in.
- Translate or change the language of any extracted content.
- Summarize long text into a shorter paraphrase; extract as-is,
  trimming only obvious filler (e.g., greeting lines in a cover letter).
- Fabricate a professional summary if none exists in the text — leave
  the summary field as empty string instead.
- Duplicate skills across multiple categories.
- Merge a Skill's full name and abbreviation into a single string.
- Invent a role/title field for Personal — it does not exist in this schema.
- Invent date fields for Education — it does not exist in this schema.

────────────────────────────────────────
OUTPUT
────────────────────────────────────────

Return ONLY valid JSON conforming exactly to the CandidateProfile
schema provided.

Do not include explanations, comments, or Markdown formatting.

Do not wrap the JSON in code fences.
"""