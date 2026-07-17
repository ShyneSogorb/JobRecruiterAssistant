JOB_EXTRACTOR_RULES = """
Extract all information present in the provided job posting text into a
JobOffer JSON object, following the schema exactly.

────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────

Extract, never invent.

The text is the single source of truth. Every field you populate must
be directly traceable to something explicitly stated in the text.

If a piece of information is not present or not clearly implied, leave
the corresponding field as null, an empty string, or an empty array, or
use the schema's designated "not specified"/"unknown" value - never
guess or fabricate a plausible-sounding value.

────────────────────────────────────────
EXTRACTION RULES
────────────────────────────────────────

Job title:
- Extract the title exactly as written, if present.
- If there is no explicit title, use the clearest short phrase from the
  text that identifies what the position is about. Do not invent a
  title that isn't grounded in the text's own wording.

Description:
- The description field must contain the original job description text,
  not a summary or rewrite.

Company:
- Extract the company/organization name only if explicitly stated.

Location:
- Extract exactly as written (city, region, country, "remote", etc.).

Target language:
- Set target_language to the ISO 639-1 code ("en" or "es") of the
  language the job posting text itself is written in.
- Base this only on the actual language of the provided text, never on
  assumptions about the company, country, or industry.
- If the text mixes languages, use the language that makes up the
  majority of the content.

Required skills / Preferred skills:
- Extract each technology, tool, programming language, certification or
  concrete requirement as an individual item, never grouped into a
  single string.
- Use canonical names for obvious variants: "React.js" -> "React",
  "Python 3.x" -> "Python".
- Strip trailing punctuation (periods, commas, semicolons) from each
  item, since these are standalone list items, not full sentences.
  "Conocimientos de programación." -> "Conocimientos de programación"
- Do not include spoken/written languages here - those belong only in
  the languages field.
- Only extract an item if the text actually states it. Do not infer a
  skill from the job title or industry alone (e.g. do not add
  "Leadership" just because the title says "Manager" unless the text
  itself mentions it).
- Default assumption: if the text does not clearly mark an item as
  mandatory (e.g. via "requisitos", "imprescindible", "required",
  "must have"), treat it as preferred_skills, not required_skills.
  Only place an item in required_skills when the text signals it is a
  hard requirement.
- Explicit preference markers (e.g. "se valorará", "preferably",
  "a plus", "nice to have") always route the item to preferred_skills.

Languages:
- Only include a language if it is explicitly stated as a requirement,
  or clearly implied by strong contextual evidence (e.g. the posting is
  written in a specific language for a local, in-person, customer-
  facing role in that language's region).
- Do not infer a language requirement you are not reasonably confident
  about. When in doubt, omit it.

Work mode / Employment type / Experience level:
- These three fields are ARRAYS, not single values. Each must be a list
  containing one or more of the allowed enum values.
- If the text explicitly or unambiguously indicates one or more values,
  include all of them (e.g. a posting offering both "remoto" and
  "híbrido" -> work_mode: ["remote", "hybrid"]).
- Distinguish between the employer offering multiple valid options
  (e.g. "remoto o híbrido, a convenir" -> work_mode: ["remote", "hybrid"],
  since both are genuinely available) versus the text being vague or
  silent about mode (-> ["unknown"]). An explicit "or" between two valid
  modes means both are offered, not that the mode is uncertain.
- If there is no information, or the text is genuinely ambiguous,
  return a single-item array with "unknown" - e.g. ["unknown"] - never
  an empty array and never a bare string.
- Do not guess based on job type, industry, or company norms.
- Do not infer experience_level from tone, salary, or general
  impression of seniority - only from an explicit title or explicit
  years-of-experience requirement.

────────────────────────────────────────
WHAT YOU MUST NOT DO
────────────────────────────────────────

Never:
- Fabricate a company name, salary, location, or requirement not present
  in the text.
- Summarize or paraphrase the description field - it must remain the
  original text.
- Translate any content out of its original language.
- Infer work_mode, employment_type, or experience_level from stereotype
  or industry norms when the text itself is silent.
- Merge distinct requirements into a single vague item, or split a
  single requirement into unrelated fragments.
- Place a non-mandatory item in required_skills just because it appears
  under a "Requisitos" heading, if the specific sentence itself signals
  it is optional or valued rather than required.
- Return work_mode, employment_type, or experience_level as a bare
  string - they must always be arrays, even with a single value.

────────────────────────────────────────
OUTPUT
────────────────────────────────────────

Return ONLY valid JSON conforming exactly to the JobOffer schema
provided.

Do not include explanations, comments, or Markdown formatting.

Do not wrap the JSON in code fences.
"""