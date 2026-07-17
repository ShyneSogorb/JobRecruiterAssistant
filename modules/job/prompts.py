from typing import Any

JOB_OFFER_JSON_RULES = """
Return ONLY valid JSON matching the provided JSON Schema.

Do not use markdown.
Do not wrap the JSON in code fences.
Do not explain anything.
Return only the JSON object.

The JobOffer object has already been partially populated using
structured data extracted from the job board.

Update this JobOffer.

Do not rebuild it from scratch.

Treat the existing values as the source of truth unless the original
job description clearly provides more accurate information or explicitly
contradicts them.

Your primary task is to populate:

- required_skills
- preferred_skills
- languages
- target_language

You may also improve:

- work_mode
- employment_type
- experience_level

ONLY when the original job description explicitly provides more accurate
information.

Never invent, infer, or guess information.

If a field cannot be improved from the description, preserve its current
value.

Never remove existing information unless the description explicitly
proves it is incorrect.

Return the complete updated JobOffer object.
"""

ATS_KEYWORDS_RULES = """
Update ONLY the ats_keywords field.

Return ONLY valid JSON matching the provided JSON Schema.

Do not modify any other field.

The JobOffer has already been parsed.

Your task is to populate ats_keywords with the terms that are most
likely to improve ATS matching for this specific job posting.

Rules:

- Extract between 10 and 30 keywords.
- Use short canonical terms.
- One keyword per list item.
- Remove duplicates.
- Preserve the original language whenever possible.
- Prefer nouns or noun phrases rather than sentences.
- Include the job title if it is meaningful.
- Include important technologies, programming languages, engines,
  frameworks, tools, methodologies, design disciplines and domain
  knowledge.
- Include concepts that recruiters commonly search for if they are
  explicitly present in the posting.
- Never invent technologies or qualifications.
- Never include complete sentences.
- Never include company benefits, perks, locations, salary,
  employment type, work mode or company names unless they are an
  essential part of the role itself.
- Keywords should maximize ATS searchability rather than summarize
  the job.

Return ONLY the list of ats-keywords.
"""


class JobPromptBuilder:
    def build_job_offer_parser(
        self,
        offer: str,
        schema: dict[str, Any],
    ) -> str:
        return f"""
{JOB_OFFER_JSON_RULES}

Current JobOffer:

{offer}

JSON Schema:

{schema}
"""
    
    def build_job_ats_extractor(
        self,
        offer: str,
    ) -> str:
        return f"""
{ATS_KEYWORDS_RULES}

Current JobOffer:

{offer}

"""