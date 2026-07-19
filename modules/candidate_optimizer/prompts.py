SKILL_RULES = """
You are a technical skills filter for a resume, given a specific job offer.

Your only task: from the candidate's skill list, select the ones that 
match or are directly related to what the job offer asks for 
(required_skills, preferred_skills, ats_keywords, or technologies 
explicitly mentioned in the job description).

Do NOT evaluate whether the candidate is a good "fit" for the role. 
Do NOT decide whether their experience is compatible or relevant to the 
position as a whole. That decision belongs to the candidate, not you.

RULES:
1. KEEP any skill that appears in, matches, or is clearly related to the 
   required_skills, preferred_skills, or ats_keywords of the job offer.
2. KEEP generic programming skills that are universally applicable to any 
   software role (e.g., Git, debugging, testing, version control) ONLY if 
   the job offer mentions or implies them.
3. REMOVE any skill that has no direct or indirect relation to what the 
   job offer asks for - regardless of whether it's a "good skill" in 
   general, belongs to a technically impressive domain, or could be 
   useful in some other context. The only question is: does this offer 
   ask for it or mention it?
4. Do not add explanations, warnings, or commentary about whether the 
   profile is a good fit. Just filter.
5. The output must be an exact subset of the received skills: do not 
   invent, rename, merge, or split any skill object.

Return ONLY the resulting skills, in the same order as the input.
"""

SOFT_SKILLS_RULES = """
You are selecting which soft skills should remain on a resume.

The provided soft skills are the ONLY source of truth.

Your task is ONLY to decide which soft skills to KEEP and which to REMOVE.

The output MUST be a strict subset of the provided soft skills.

Each returned skill object MUST be copied exactly as it appears in the input.

Do NOT:
- invent skills
- rename skills
- rewrite skills
- merge skills
- split skills
- modify any field
- create new objects

Keep a soft skill if it is:
- explicitly required by the job,
- explicitly preferred by the job,
- clearly useful for performing the role,
- valuable for ATS matching,
- relevant to the responsibilities described in the job offer.

Remove a soft skill only if it is:
- purely generic filler with no connection to the job's responsibilities
  (e.g. vague traits not supported by anything in the job description),
- unrelated to the responsibilities described,
- clearly redundant with another soft skill already kept that expresses the
  same idea.

When uncertain whether a soft skill helps or hurts the application, KEEP it -
soft skills rarely hurt an application, so the bar for removal is being
clearly generic or clearly irrelevant, not merely "not explicitly mentioned".

Return ONLY the remaining soft skills.
"""

TRANSFERABLE_SKILLS_RULES = """
You are selecting which transferable skills should remain on a resume.

The provided transferable skills are the ONLY source of truth.

Your task is ONLY to decide which transferable skills to KEEP and which to
REMOVE.

The output MUST be a strict subset of the provided transferable skills.

Each returned skill object MUST be copied exactly as it appears in the input.

Do NOT:
- invent skills
- rename skills
- rewrite skills
- merge skills
- split skills
- modify any field
- create new objects
- assume technical compatibility or incompatibility between tools,
  domains, or industries that is not stated in the job offer

Transferable skills describe technical knowledge, engineering practices,
methodologies or problem-solving abilities that can be applied across
different technologies, engines or projects.

Keep a transferable skill if it is:
- explicitly required by the job,
- explicitly preferred by the job,
- closely related to the responsibilities of the role,
- valuable regardless of the specific technologies used,
- likely to strengthen ATS matching for this position.

Remove a transferable skill only if you can point to a concrete reason it
belongs to a domain with no plausible connection to this role - do not
remove a skill based on a guess about technical incompatibility.

When uncertain, KEEP the skill - transferable skills are, by definition,
meant to apply broadly, so the bar for removing one should be higher than
for a narrowly technical skill.

Return ONLY the remaining transferable skills.
"""

LANGUAGES_RULES = """
You are selecting which languages should remain on a resume.

The provided languages are the ONLY source of truth.

Your task is ONLY to remove languages.

Do NOT:
- add languages
- rename languages
- modify proficiency levels
- merge languages
- split languages
- rewrite anything

Keep only the languages that strengthen the candidate's application for
the target job.

Prefer languages explicitly required by the job posting.

Otherwise, prefer languages that are likely to be professionally useful
for the role (e.g. the language of the job's location, or widely used
business languages).

When uncertain whether a language adds value, KEEP it - listing an extra
language rarely harms an application.

Remove languages that add little or no value for this specific job.

Return the remaining languages in their original format and order.
"""

ADDITIONAL_INFO_RULES = """
You are selecting which additional information should remain on a resume.

The provided entries are the ONLY source of truth.

Your task is ONLY to remove entries.

Do NOT:
- add entries
- rewrite entries
- shorten entries
- merge entries
- split entries
- modify wording

Keep only entries that strengthen the candidate's application for the
target job.

Remove entries only if they are clearly unrelated to the job's domain,
responsibilities, or transferable skills the job values.

When uncertain whether an entry adds value, KEEP it.

Return the remaining entries in their original wording and order.
"""

PROJECT_RULES = """
You are selecting which projects should remain on a resume.

The provided projects are the ONLY source of truth.

Your task is to decide which projects to KEEP and which to REMOVE, and,
within each project you keep, which achievements to KEEP and which to
REMOVE.

The output MUST be a strict subset of the provided projects: you may drop
whole projects, and you may drop individual achievements from a project you
keep, but you may never add, invent, or alter anything.

Each returned project object, and each returned achievement inside it, MUST
be copied exactly as it appears in the input - untouched, field for field.

Do NOT:
- invent projects or achievements
- rename a project's name
- rewrite an achievement's context/action/impact/metric wording
- merge two achievements into one
- split one achievement into two
- merge two projects into one
- modify the `technologies` or `date` fields
- create new objects
- infer experience the candidate does not have
- assume technical compatibility or incompatibility between tools,
  engines, or domains that is not stated in the job offer

Keep a project if it is:
- built with technologies explicitly required or preferred by the job,
- demonstrating a skill or problem domain closely related to the job,
- likely to improve ATS keyword matching for this position,
- valuable evidence of relevant technical ability for this specific role.

Remove a project entirely if it is:
- unrelated to the position,
- built with technologies from a completely different domain that adds no
  value here,
- unlikely to help ATS matching or the recruiter's evaluation for this role.

When uncertain whether a project's technology domain is relevant, KEEP the
project - only remove it if the mismatch is unambiguous and explainable
without external assumptions.

Within a project you decide to keep, remove an individual achievement if it:
- describes a feature or detail unrelated to what makes this project
  relevant to the job,
- is redundant with another achievement already kept in the same project,
- adds length without adding relevance for this specific position.

Never remove every achievement from a project you are keeping - if nothing
in a project's achievements is worth keeping, remove the whole project
instead of leaving it with an empty achievements list.

Return ONLY the remaining projects, each with its remaining achievements.
"""

SUMMARY_RULES = """
Write a professional resume summary tailored to the provided job offer.

Return ONLY the summary text as the "string" field of the provided JSON
schema.

Requirements:

- Write a single paragraph.
- Keep it between 40 and 80 words.
- Never exceed 4 lines in a typical resume.
- Tailor the summary specifically to the target position.
- Base it ONLY on the candidate projects and the job offer.
- Do not invent experience, skills, achievements, or qualifications.
- Do not state or imply a number of years of experience unless that number
  is explicitly given in the candidate's experience dates - do not
  calculate or round it yourself.
- Emphasize the experience and competencies that best match the job.
- Naturally incorporate important keywords from the job offer,
  especially required skills, preferred skills, technologies,
  methodologies, and the job title when appropriate.
- Prioritize ATS-friendly wording while remaining natural to a human
  reader.
- Do not use first person ("I", "my", "me").
- Do not use generic filler such as "hard-working", "passionate",
  "motivated", "team player", or similar unless directly supported by
  the candidate information.
- Do not mention skills or technologies that are not present in the
  candidate projects.
"""
EXPERIENCE_RULES = """
You are selecting which work experience entries should remain on a resume.

The provided experience entries are the ONLY source of truth.

Your task is to decide which experience entries to KEEP and which to REMOVE,
and, within each entry you keep, which achievements to KEEP and which to
REMOVE.

The output MUST be a strict subset of the provided experience entries: you
may drop whole entries, and you may drop individual achievements from an
entry you keep, but you may never add, invent, or alter anything.

Each returned experience object, and each returned achievement inside it,
MUST be copied exactly as it appears in the input - untouched, field for
field.

Do NOT:
- invent experience entries or achievements
- rename a job title, company, or dates
- rewrite an achievement's context/action/impact/metric wording
- merge two achievements into one
- split one achievement into two
- merge two experience entries into one
- change `is_professional`
- create new objects
- infer experience the candidate does not have
- assume technical compatibility or incompatibility between tools,
  engines, or domains that is not stated in the job offer

SPECIAL RULE - PAID ANIMAL SHELTER (PROTECTORA) JOB:
If an experience entry is the PAID animal shelter / protectora job
(is_professional is true and the role is about animal care/shelter work),
you may only either keep it as-is or remove it entirely - never move it,
rename it, or alter its achievements beyond the normal
keep/remove-achievement rules below. This entry follows the exact same
relevance judgment as any other entry: keep it only if the target job
genuinely benefits from it (e.g. the job itself involves animal care,
physical work, or similarly transferable responsibilities); otherwise remove
it entirely, the same as you would for an unrelated software job.

Keep an experience entry if it demonstrates:
- technologies, tools, or responsibilities explicitly required or preferred
  by the job,
- a role, industry, or seniority level closely related to the position,
- transferable responsibilities valuable for evaluating this candidate for
  this specific role,
- content likely to improve ATS keyword matching for this position.

Remove an experience entry entirely if it is:
- unrelated to the position and offers no transferable value,
- redundant with a stronger, more relevant entry already kept,
- unlikely to help ATS matching or the recruiter's evaluation for this role.
When uncertain whether a project's technology domain is relevant, KEEP the
project - only remove it if the mismatch is unambiguous and explainable
without external assumptions.

Within an experience entry you decide to keep, remove an individual
achievement if it:
- describes a responsibility unrelated to what makes this entry relevant to
  the job,
- is redundant with another achievement already kept in the same entry,
- adds length without adding relevance for this specific position.

Never remove every achievement from an experience entry you are keeping - if
nothing in an entry's achievements is worth keeping, remove the whole entry
instead of leaving it with an empty achievements list.

Return ONLY the remaining experience entries, each with its remaining
achievements.
"""

EDUCATION_RULES = """
You are selecting which education entries should remain on a resume.

The provided education entries are the ONLY source of truth.

Your task is ONLY to decide which whole education entries to KEEP and which
to REMOVE. Unlike experience or projects, you do NOT prune individual
achievements within an education entry you keep - an education entry is kept
or removed as a whole, exactly as given.

The output MUST be a strict subset of the provided education entries.

Each returned education object MUST be copied exactly as it appears in the
input - untouched, field for field, including all of its achievements.

Do NOT:
- invent education entries
- rename an institution, degree, or field
- rewrite, add, or remove individual achievements within an entry you keep
- merge two education entries into one
- split one education entry into two
- create new objects
- infer credentials the candidate does not have

Keep an education entry if it is:
- the credential or field of study explicitly required or preferred by the
  job,
- closely related to the domain, technology, or seniority level of the
  position,
- likely to improve ATS keyword matching for this position (e.g. a degree
  title or field that overlaps with the job's required background),
- reasonable evidence of foundational knowledge relevant to this role, even
  if not a perfect match.

Remove an education entry entirely if it is:
- in a field completely unrelated to the position and to any transferable
  skill the job values,
- redundant or clearly superseded by a more advanced, more relevant entry
  already kept (e.g. an intermediate-level credential in the exact same
  field as a higher one already kept, when space and relevance both favor
  dropping the lower one),
- unlikely to help ATS matching or the recruiter's evaluation for this role.

When in doubt, prefer keeping an education entry over removing it - a degree
being somewhat generic is a weaker reason to remove it than being genuinely
unrelated to the job's domain.

Return ONLY the remaining education entries, complete and unmodified.
"""

class CandidateOptimizerPrompts:
    def build_skill_optimizer(self, job: str, skills: str) -> str:
        return f"""
{SKILL_RULES}

Job offer:
{job}

Candidate technical skills:
{skills}
"""

    def build_soft_skill_optimizer(self, job: str, skills: str) -> str:
        return f"""
{SOFT_SKILLS_RULES}

Job offer:
{job}

Candidate soft skills:
{skills}
"""
    
    def build_transferable_skill_optimizer(self, job: str, skills: str) -> str:
        return f"""
{TRANSFERABLE_SKILLS_RULES}

Job offer:
{job}

Candidate soft skills:
{skills}
"""
    
     
    def build_project_optimizer(self, job: str, projects: str) -> str:
        return f"""
{PROJECT_RULES}
 
Job offer:
{job}
 
Candidate projects:
{projects}
"""
 
    def build_experience_optimizer(self, job: str, experience: str) -> str:
        return f"""
{EXPERIENCE_RULES}
 
Job offer:
{job}
 
Candidate experience:
{experience}
"""
 
    def build_education_optimizer(self, job: str, education: str) -> str:
        return f"""
{EDUCATION_RULES}
 
Job offer:
{job}
 
Candidate education:
{education}
"""
    
    def build_language_optimizer(self, job: str, languages: str) -> str:
        return f"""
{LANGUAGES_RULES}
 
Job offer:
{job}
 
Candidate languages:
{languages}
"""
    
    def build_aditional_optimizer(self, job: str, aditional: str) -> str:
        return f"""
{ADDITIONAL_INFO_RULES}
 
Job offer:
{job}
 
Candidate aditional info:
{aditional}
"""
    
         
    def build_optimized_summary(self, job: str, candidate: str) -> str:
        return f"""
{SUMMARY_RULES}
 
Job offer:
{job}
 
Candidate:
{candidate}
"""