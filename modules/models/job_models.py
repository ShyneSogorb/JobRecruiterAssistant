from typing import Annotated
from pydantic import BaseModel, Field
import sqlite3
from enum import StrEnum

from modules.models.simple_models import TargetLanguage


class SalaryPeriod(StrEnum):
    unknown = "unknown"
    hour = "hour"
    month = "month"
    year = "year"


class SalaryCurrency(StrEnum):
    euros = "euros"
    american_dollars = "american_dollars"
    zloty = "zloty"
    pounds = "pounds"
    yen = "yen"


class Salary(BaseModel):
    currency: SalaryCurrency | str | None = Field(
        default=None,
        description="Currency exactly as implied by the text. Use one of "
        "the enum values if it matches; otherwise use the literal currency "
        "name/symbol from the text as a string. Leave null if no currency "
        "is stated - do not force a value.",
    )
    minimum: float | None = Field(
        default=None,
        description="Minimum salary figure exactly as stated. Null if the "
        "text gives only a single figure or no figure at all.",
    )
    maximum: float | None = Field(
        default=None,
        description="Maximum salary figure exactly as stated. Null if the "
        "text gives only a single figure or no figure at all.",
    )
    period: SalaryPeriod = Field(
        default=SalaryPeriod.unknown,
        description="Pay period the figures refer to (per hour/month/year). "
        "Use 'unknown' if the text states a figure without a clear period.",
    )


class JobModality(StrEnum):
    unknown = "unknown"
    onsite = "onsite"
    hybrid = "hybrid"
    remote = "remote"


class EmploymentType(StrEnum):
    unknown = "unknown"
    full_time = "full_time"
    part_time = "part_time"
    contract = "contract"
    internship = "internship"
    freelance = "freelance"
    temporary = "temporary"


class ExperienceLevel(StrEnum):
    unknown = "unknown"
    intern = "intern"
    junior = "junior"
    mid = "mid"
    senior = "senior"
    lead = "lead"





class LanguageRequirement(BaseModel):
    language: str = Field(description="Name of the spoken/written language.")
    level: str | None = Field(
        default=None,
        description="Proficiency level exactly as stated (e.g. 'Native', "
        "'Fluent', 'B2'). Null if the text requires the language but does "
        "not specify a level.",
    )

SKILL_DESC = """
A skill is any concrete technology, framework, engine, programming
language, software, methodology, workflow, design discipline,
certification, domain knowledge, or other professional competency
explicitly required or desired by the posting.

Treat professional disciplines and areas of expertise as skills.

Extract every qualifying skill individually.

Store one short canonical term per list item.

Do not output duplicate skills.

Keep the original order of appearance whenever possible.

Do not combine multiple independent skills into a single item.

When a sentence contains multiple independent technologies or
competencies, extract each one separately.

Normalize names whenever possible.

Examples:

- UE5 -> Unreal Engine
- UE5 Blueprints -> Unreal Engine, Blueprints
- React.js -> React
- Python 3 -> Python
- C++17 -> C++

If the posting requires experience with a technology, tool, engine,
workflow, methodology, or professional discipline, extract that
technology or discipline itself as a skill.

Each skill must be a short canonical term, never a sentence or
paragraph.

Never include spoken or written languages.
"""

class JobOffer(BaseModel):
    id: str = Field(
        description="Id of the offer, NEVER MODIFY this, just copy it"
    )

    company: str = Field(
        description="Company or organization name exactly as stated in the "
        "text. Empty string if no name is explicitly given - do not invent "
        "or guess one from context (e.g. from an email domain or industry "
        "description)."
    )

    role: str = Field(
        description="Job role exactly as written in the text. If there is "
        "no explicit role, use the more suitable role "
        "that identifies what the position is about, without inventing an "
        "unrelated title."
    )

    location: str = Field(
        description="Location exactly as written (city, region, country, "
        "or 'remote'). Empty string if not stated."
    )

    url: str = Field(
        description="Application URL exactly as it appears in the text "
        "(e.g. a LinkedIn, Indeed, or Glassdoor link). Empty string if none "
        "is present."
    )

    target_language: TargetLanguage = Field(
        description="ISO 639-1 code of the language the job posting text "
        "itself is written in. Base this only on the actual language of "
        "the text, never on assumptions about the company or location. If "
        "the text mixes languages, use the one that makes up the majority "
        "of the content."
    )

    ats_keywords: list[str] = Field(
        default_factory=list,
        description=(
            "Canonical ATS search keywords representing the position. "
            "Include the most relevant job titles, technologies, programming "
            "languages, engines, frameworks, tools, methodologies, design "
            "disciplines and domain concepts explicitly present in the job "
            "posting. Store one short canonical keyword per item. Remove "
            "duplicates. Never include sentences, company names, benefits, "
            "locations, salary information or generic soft skills."
        ),
    )

    work_mode: list[JobModality] = Field(
        default_factory=list,
        description="All work modes explicitly offered by this posting. "
        "A posting can offer more than one - if the text says 'remoto o "
        "híbrido', include both 'remote' and 'hybrid', since an explicit "
        "'or' between two modes means both are genuinely available, not "
        "that the mode is uncertain. Use ['unknown'] only when the text "
        "gives no information at all about work mode - never leave this "
        "empty and never guess based on job type or industry norms.",
    )

    employment_type: list[EmploymentType] = Field(
        default_factory=list,
        description="All employment types explicitly stated as offered by "
        "this posting (a posting may offer more than one). Use ['unknown'] "
        "only when the text gives no information at all - never leave this "
        "empty and never guess based on job type or industry norms.",
    )

    experience_level: list[ExperienceLevel] = Field(
        default_factory=list,
        description="Experience level(s) required, inferred ONLY from an "
        "explicit title (e.g. 'Senior Developer') or an explicit years-of-"
        "experience requirement stated in the text - never from tone, "
        "salary, or a general impression of seniority. Use ['unknown'] "
        "when the wording does not clearly support a specific level.",
    )

    description: str = Field(
        description="The original job posting text, verbatim and complete. "
        "Never summarized, rewritten, shortened, or paraphrased."
    )

    required_skills: list[str] = Field(
        default_factory=list,
        description=(
            "Professional competencies explicitly required by the job posting. "
            "Extract only mandatory requirements, such as those introduced by "
            "'required', 'must', 'essential', 'imprescindible', or equivalent. "
            + SKILL_DESC
        ),
    )

    preferred_skills: list[str] = Field(
        default_factory=list,
        description=(
            "Professional competencies explicitly described as optional, "
            "preferred, desirable, beneficial, or 'nice to have'. Also place "
            "here any competency whose mandatory status cannot be determined "
            "with confidence from the text. "
            + SKILL_DESC
        ),
    )

    languages: list[LanguageRequirement] = Field(
        default_factory=list,
        description="Spoken/written languages explicitly required, or "
        "clearly implied by strong contextual evidence (e.g. a local, "
        "in-person, customer-facing role written in a specific language). "
        "Omit a language entirely if you are not reasonably confident it "
        "is actually a requirement - do not infer from the posting's own "
        "language alone.",
    )

    salary: Salary | None = Field(
        default=None,
        description="Salary information only if explicitly stated in the "
        "text. Null if no salary figure or range is given.",
    )

class EJobState(StrEnum):
    RAW = "raw"
    PARSED = "parsed"
    READY = "ready"
    APPLIED = "applied"

class JobApplication(BaseModel):
    id: str
    job: JobOffer
    cv: str | None = None
    cv_path: str | None = None
    hiring_manager: str | None = None
    cover_letter:str | None = None
    state: EJobState
    salary: Salary | None = None
    score: float | None = None
