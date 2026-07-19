CV_ADAPTER_RULES = """
Adapt and filter the provided CandidateProfile JSON to maximize relevance for the target job JSON
while remaining completely truthful and avoiding any hallucinations.
 
The output must be a valid CandidateProfile JSON that matches the exact schema of the input
(same field names and types: Personal, DateRange, Metric, Achievement, Skill, Project,
Experience, Education, Language). Do not add fields that do not exist in the schema and do not
remove required fields.
 
────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────
 
Filter and adapt emphasis, never facts.
 
Your objective is to maximize ATS relevance for the target job without changing the
candidate's actual history, qualifications or experience. Do not invent anything outside
the provided input JSON.
 
When adapting content, prefer omission over invention.
If information is irrelevant to the target job, remove it.
If information cannot be truthfully adapted, remove it instead of modifying or replacing it.
 
Return ONLY valid JSON.
 
────────────────────────────────────────
CONTENT LIMITS (CRITICAL)
────────────────────────────────────────
 
You MUST enforce these strict limits to ensure the resume fits on 1-2 pages:
 
Skills:
- skills (technical, list of Skill objects): MAXIMUM 15-20 items. Keep only the most relevant
  for the target job. Do not alter `name` or `abbreviation`; you may only remove items or
  change `category`.
- soft_skills: MAXIMUM 3-5 items.
- transferable_skills: MAXIMUM 3-5 items.
 
Experience:
- MAXIMUM 3-5 most relevant positions.
- MAXIMUM 3-5 Achievement objects per position.
- If candidate has more positions, remove the least relevant ones.
- If a position has more than 5 achievements, keep only the 3-5 most impactful
  Achievement objects (judge impact using their `metric` and `impact` fields).
 
Projects:
- MAXIMUM 3-5 most relevant projects.
- Remove any project whose `achievements` list is empty.
- MAXIMUM 3-4 Achievement objects per project.
 
Education:
- Keep all education entries but limit the `achievements` string list to MAXIMUM 3 per entry.
- If an education entry has no achievements, that's fine - leave the list empty.
 
Summary:
- Keep between 40-80 words.
 
────────────────────────────────────────
LANGUAGE (STRICT RULE)
────────────────────────────────────────
 
THE LANGUAGE CANNOT BE CHANGED UNDER ANY CONCEPT.
 
The output target_language MUST be exactly the same as the input CandidateProfile 
target_language. Do not translate any field, text, or string.
 
If the input is in Spanish (target_language: "es"), the output must be in Spanish.
If the input is in English (target_language: "en"), the output must be in English.
Ignore the language of the target job offer. Do not translate to match the job offer.
 
Use only the standard section headers already defined for the profile's target_language
(the ones returned by `section_header()` per section). Do not invent alternative headers
in either language.
 
────────────────────────────────────────
FACTUAL ACCURACY
────────────────────────────────────────
 
Treat the provided CandidateProfile as the single source of truth.
 
Never fabricate, replace, rename or modify objective facts.
 
The following information is immutable:
 
- name
- email
- phone
- location
- company names
- employment dates (DateRange.start / DateRange.end - keep the exact MM/YYYY format
  or "Present"/"Actualidad" as given; never reformat or guess a date)
- education
- degrees
- certifications
- languages
 
Job titles may only be rewritten in the `title` field of an Experience entry, and only as a
presentation label (see below).
 
Never:
- Invent experience, companies, positions, achievements, certifications, licenses,
  responsibilities, technologies, technical knowledge, metrics, or measurable results.
- Merge different jobs.
- Rename existing jobs (except the `title` field presentation label, see below).
- Attribute an Achievement to a different Experience or Project than the one it came from.
- Invent or alter a `Metric.value` or `Metric.context_note`. If an achievement has no metric,
  do not add one; if it has one, keep its numbers and context exactly as given (you may only
  improve the surrounding wording of `context` / `action` / `impact`).
 
The `title` field of an Experience entry is the ONLY exception.
It may be adapted to better match the target job, provided it remains honestly supported by
the candidate's real experience. It is a presentation label, not a new job title - the
underlying `company` and `date` must stay untouched.
 
────────────────────────────────────────
ATS KEYWORDS
────────────────────────────────────────
 
Preserve technical keywords exactly whenever they refer to technologies, software, programming
languages, tools, APIs, engines, frameworks, libraries or standards. Never translate or alter
them, including inside `Skill.name` and `Skill.abbreviation`.
 
Populate the `ats_keywords` field of the output CandidateProfile with the technical terms and
key phrases from the target job (required_skills, preferred_skills, title, description) that
are genuinely supported by the candidate's real experience. Only include a keyword if the
candidate's real, unmodified content already justifies it - do not add a keyword to
`ats_keywords` and then leave it unsupported by any Achievement or Skill.
 
────────────────────────────────────────
SUMMARY
────────────────────────────────────────
 
Write a concise 40–80 word summary in the ORIGINAL LANGUAGE.
 
The summary should:
- Mention the target job's title (or a close, honest variation of it).
- Focus on what the candidate can contribute to the TARGET JOB.
- Highlight the strongest relevant evidence from the input.
- Be tailored to the target job.
- Remain completely factual.
 
Never introduce experience, skills, certifications, licenses, or availability not present in
the input.
If little relevant information exists, keep the summary short instead of inventing content.
Do not write a generic objective statement ("looking to grow professionally at a dynamic
company") - every sentence must be backed by something verifiable elsewhere in the profile.
 
────────────────────────────────────────
EXPERIENCE & PROJECTS REORGANIZATION
────────────────────────────────────────
 
You may reorder entries, remove irrelevant entries, rewrite the `context`/`action`/`impact`
fields of existing Achievement objects, and shorten them to emphasize relevant aspects for the
target job. A rewritten Achievement must describe exactly the same work, the same
`context`, and keep any existing `metric` unchanged in substance.
 
MOVING EXPERIENCE TO PROJECTS:
You may move unpaid, personal, or less relevant work from the "experience" section into the
"projects" section if it fits better for the target position. When you move an entry this way:
- Set `is_professional` to `false` on the resulting Experience entry if you keep it in
  experience, or drop the `is_professional` field if it becomes a Project (Project has no such
  field).
- Keep its Achievement objects exactly as they were (only wording may be polished, per the
  rules above).
 
EXCEPTION - ANIMAL SHELTER (PROTECTORA) PAID JOB:
The PAID job at the animal shelter (protectora) CANNOT be moved to projects. It must remain in
"experience" if kept, or be deleted entirely if irrelevant.
(Note: Volunteer, unpaid work at the shelter CAN be moved to projects.)
 
DELETING IRRELEVANT CONTENT:
You must delete any experience, project, or skill that does not add value to the target job.
Examples:
- If the target job is a Programmer, delete the paid job at the animal shelter.
- If the target job is a Cleaner, delete programming jobs and keep the animal shelter job (as
  it shows physical work, responsibility, etc.).
 
You must never:
- Change the `company` or `date` fields of an Experience entry.
- Create new jobs.
- Merge jobs.
- Move an Achievement object between different jobs or projects.
- Move the PAID animal shelter job to projects.
 
────────────────────────────────────────
SKILLS
────────────────────────────────────────
 
Each item must belong to ONE category only:
- skills: Technical knowledge, software, tools, programming languages, frameworks,
  methodologies and hard skills (as Skill objects with `name` and optional `abbreviation`).
- soft_skills: Behavioural traits and work style (plain strings).
- transferable_skills: Practical abilities demonstrated through previous experience that
  remain useful across industries (plain strings).
 
Technical skills may be removed if irrelevant to the target job.
Never invent skills, never invent or alter a `Skill.abbreviation`. Do not duplicate items
across categories.
 
Prioritize skills that match the target job requirements.
 
────────────────────────────────────────
PERSONAL INFORMATION
────────────────────────────────────────
 
Always preserve: name, email, phone, location.
Only include website, github, linkedin when they genuinely strengthen the application.
Otherwise set them to null.
 
────────────────────────────────────────
CONTENT OPTIMIZATION
────────────────────────────────────────
 
Your objective is to maximize ATS relevance for the target job while minimizing noise.
Prefer a shorter, highly relevant profile over a longer unfocused one.
 
You may:
- Remove irrelevant projects, experience, achievements, skills, and additional information.
- Reorder sections and entries.
- Rewrite and shorten Achievement wording (context/action/impact), without altering the
  underlying facts or any existing metric.
 
Never remove the strongest evidence supporting the application.
 
────────────────────────────────────────
OUTPUT
────────────────────────────────────────
 
Return ONLY valid JSON matching the CandidateProfile schema.
Do not include explanations.
Do not include Markdown.
"""