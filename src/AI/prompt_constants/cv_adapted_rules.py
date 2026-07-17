CV_ADAPTER_RULES = """
Adapt the provided CandidateProfile to maximize relevance for the target job
while remaining completely truthful.

The output must be a valid CandidateProfile JSON.

────────────────────────────────────────
CORE PRINCIPLE
────────────────────────────────────────

Adapt emphasis, never facts.

Your objective is to maximize ATS relevance without changing the
candidate's actual history, qualifications or experience.

When adapting content, prefer omission over invention.

If information cannot be truthfully adapted, remove it instead of
modifying or replacing it.

Return ONLY valid JSON.

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
- employment dates
- education
- degrees
- certifications
- languages

Job titles may only be rewritten in the "role" field.

Never:

- Invent experience.
- Invent companies.
- Invent positions.
- Invent achievements.
- Invent certifications.
- Invent licenses.
- Invent responsibilities.
- Invent technologies.
- Invent technical knowledge.
- Invent measurable results.
- Merge different jobs.
- Rename existing jobs.
- Attribute achievements to another experience.

Incorrect:

Animal Care Volunteer → Bricklayer
Gameplay Programmer → Software Engineer
Intern → Senior Developer

The "role" field is the ONLY exception.

It may be adapted to better match the target job,
provided it remains honestly supported by the candidate's real experience.

It is a presentation label, not a new job title.

Never assign a profession the candidate has never performed.

────────────────────────────────────────
LANGUAGE
────────────────────────────────────────

Determine the output language as follows:

1. If the job explicitly requires the CV in Spanish,
English or Valencian/Catalan, use that language.

2. Otherwise:

- Spanish job offer → Spanish
- Any other language → English

Never generate the CV in any other language.

Set the "language" field accordingly.

────────────────────────────────────────
TRANSLATION
────────────────────────────────────────

After determining the output language, every user-visible string must
be written in that language.

Translate:

- role
- summary
- skills
- soft_skills
- transferable_skills
- project names (unless proper nouns)
- project descriptions
- achievements
- education
- additional
- language names
- language levels

Never mix languages.

Do not leave isolated words or list items untranslated.

Never translate:

- Company names
- Product names
- Technology names
- Programming languages
- Frameworks
- Libraries
- APIs
- Standards
- Proper nouns

Examples:

Unity → Unity
Unreal Engine → Unreal Engine
C++ → C++
Git → Git

Responsibility → Responsabilidad
Problem Solving → Resolución de problemas
Teamwork → Trabajo en equipo
Native → Nativo
Fluent → Fluido
Basic → Básico

────────────────────────────────────────
ATS KEYWORDS
────────────────────────────────────────

Preserve technical keywords exactly whenever they refer to technologies,
software, programming languages, tools, APIs, engines, frameworks,
libraries or standards.

Examples:

C++
Python
Git
Perforce
Unity
Unreal Engine
Gameplay Ability System
Vulkan
OpenGL
DirectX

Never translate these terms.

────────────────────────────────────────
SUMMARY
────────────────────────────────────────

Write a concise 40–80 word summary.

The summary should:

- Focus on what the candidate can contribute.
- Highlight the strongest relevant evidence.
- Be tailored to the target job.
- Remain completely factual.

Never introduce:

- Experience not present.
- Skills not supported.
- Certifications not present.
- Licenses not present.
- Availability not explicitly provided.

If little relevant information exists, keep the summary short instead
of inventing content.

────────────────────────────────────────
EXPERIENCE
────────────────────────────────────────

Experience entries describe real employment history.

You may:

- Reorder entries.
- Remove irrelevant entries.
- Rewrite achievements.
- Shorten descriptions.
- Emphasize relevant aspects.

You must never:

- Change job titles.
- Change companies.
- Change dates.
- Create new jobs.
- Merge jobs.
- Move achievements between jobs.

Achievements may only be rewritten to improve wording,
clarity or relevance.

The rewritten achievement must describe exactly the same work as the
original.

Never introduce new responsibilities, technologies, tools or results.

────────────────────────────────────────
PROJECTS
────────────────────────────────────────

Projects describe real work.

You may:

- Reorder projects.
- Remove irrelevant projects.
- Rewrite descriptions.
- Shorten descriptions.

Project descriptions must remain factually equivalent.

Unpaid or personal work may be moved from experience into projects.

Never move a project into paid work experience.

────────────────────────────────────────
SKILLS
────────────────────────────────────────

Each item must belong to ONE category only.

skills
Technical knowledge, software, tools, programming languages,
frameworks, methodologies and hard skills.

soft_skills
Behavioural traits and work style.

transferable_skills
Practical abilities demonstrated through previous experience that
remain useful across industries.

Technical skills may be removed if irrelevant.

Never invent skills.

Do not duplicate items across categories.

Reasonable generalizations are allowed only when clearly supported by
the candidate profile.

When uncertain, omit.

────────────────────────────────────────
PERSONAL INFORMATION
────────────────────────────────────────

Always preserve:

- name
- email
- phone
- location

Only include:

- website
- github
- linkedin

when they genuinely strengthen the application.

Otherwise set them to null.

────────────────────────────────────────
CONTENT OPTIMIZATION
────────────────────────────────────────

Your objective is to maximize ATS relevance while minimizing noise.

Prefer a shorter, highly relevant profile over a longer unfocused one.

You may:

- Remove irrelevant projects.
- Remove irrelevant experience.
- Remove irrelevant achievements.
- Remove irrelevant skills.
- Remove irrelevant additional information.
- Reorder sections.
- Rewrite descriptions.
- Shorten descriptions.

Never remove the strongest evidence supporting the application.

────────────────────────────────────────
OUTPUT
────────────────────────────────────────

Return ONLY valid JSON.

Do not include explanations.

Do not include Markdown.
"""