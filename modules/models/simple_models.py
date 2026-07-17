import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ListString(BaseModel):
    array: list[str] = Field(default_factory=list)


TargetLanguage = Literal["en", "es"]

# "Classic" section headings recommended by Kickresume because ATS systems
# recognize them reliably. The renderer should use (a faithful translation
# of) these labels instead of inventing creative headings.
STANDARD_SECTION_HEADERS: dict[str, dict[TargetLanguage, str]] = {
    "personal": {"en": "Personal Information", "es": "Información personal"},
    "summary": {"en": "Summary", "es": "Resumen"},
    "skills": {"en": "Skills", "es": "Habilidades"},
    "experience": {"en": "Work Experience", "es": "Experiencia laboral"},
    "projects": {"en": "Projects", "es": "Proyectos"},
    "education": {"en": "Education", "es": "Formación"},
    "languages": {"en": "Languages", "es": "Idiomas"},
    "additional": {"en": "Additional Information", "es": "Información adicional"},
}

_DATE_RE = re.compile(r"^(0[1-9]|1[0-2])/\d{4}$")  # MM/YYYY, 2 digits required


class Personal(BaseModel):
    """
    Contact information. It is modeled as its own section (not as a header/footer)
    because, according to Kickresume, many ATS systems do not read content placed
    in document headers or footers.
    """

    name: str
    location: str
    email: str
    phone: str
    website: str | None = None
    linkedin: str | None = None
    github: str | None = None
    # The generic "role" field has been removed from here: the target position now lives
    # in CandidateProfile.target_role because it should be repeated in the summary
    # (Kickresume step 4) and is not considered contact information.


class DateRange(BaseModel):
    """
    Single, explicit date format (MM/YYYY with 2 digits), exactly as
    recommended by Kickresume so ATS parsing does not fail because of
    inconsistencies such as "3/2022" vs "03/2022".
    "Present" / "Current" are accepted as values for `end`.
    """

    start: str
    end: str  # may be an MM/YYYY date or "Present" / "Current"

    @field_validator("start")
    @classmethod
    def _validate_start(cls, v: str) -> str:
        if not _DATE_RE.match(v):
            raise ValueError(f"'{v}' must use the MM/YYYY format, e.g. '03/2022'")
        return v

    @field_validator("end")
    @classmethod
    def _validate_end(cls, v: str) -> str:
        if v.lower() in {"present", "actualidad", "presente"}:
            return v
        if not _DATE_RE.match(v):
            raise ValueError(
                f"'{v}' must be MM/YYYY or 'Present'/'Current'"
            )
        return v
    
class Metric(BaseModel):
    """
    An impact metric MUST ALWAYS be accompanied by the context that makes it
    understandable.
    Real example from the unpacklo repository: "5 ms frame times" means nothing without
    stating on which hardware (Core i7-5820k / GTX 970) and with how many agents/objects.
    """

    value: str  # e.g. "5 ms frame time", "150 MB saved", "17k physics bodies"
    context_note: str  # e.g. "on Core i7-5820k / GTX 970, 275 AI agents, single-threaded"


class Achievement(BaseModel):
    """
    Replaces the old standalone `achievements: StringList`.

    Enforcing three separate fields (instead of a single free-form string) is the way
    to apply the central advice from the unpacklo repository: most resumes fail
    because their bullet points are only "verb + noun" without explaining the real problem
    or the result. Here it is not possible to fill in `action` without also thinking about
    `context` and `impact`.
    """

    context: str  # the real problem/constraint: "the engine loaded 14,800 loose files..."
    action: str  # what you specifically did (not what the team/company did)
    impact: str | None = None  # textual result, for cases without a hard metric
    metric: Metric | None = None  # metric + context, when quantifiable data exists
    keywords: ListString = Field(default_factory=ListString)
    # ^ keywords from the job posting that this bullet helps reinforce
    # (Kickresume: repeat relevant keywords 2–3 times throughout the resume).

    def render(self) -> str:
        """
        Builds the final bullet point as a single sentence, following the
        Context -> Action -> Impact pattern used by Dale Kim in his "good"
        examples (e.g. the pack file format bullet).
        """
        parts = [self.context.strip().rstrip("."), self.action.strip().rstrip(".")]
        sentence = ". ".join(p for p in parts if p) + "."
        if self.metric:
            sentence += f" {self.metric.value} ({self.metric.context_note})."
        elif self.impact:
            sentence += f" {self.impact.strip().rstrip('.')}."
        return sentence


class Skill(BaseModel):
    """
    Full name + optional abbreviation, because Kickresume recommends using both
    since some ATS systems only recognize the abbreviation (or only the full name).
    Examples from this profile: "Structure of Arrays" / "SoA",
    "Single Instruction, Multiple Data" / "SIMD".
    """

    name: str
    abbreviation: str | None = None
    category: str | None = None  # e.g. "Engines", "Languages", "Tools"

    def display(self) -> str:
        if self.abbreviation:
            return f"{self.name} ({self.abbreviation})"
        return self.name


class Project(BaseModel):
    name: str
    description: str
    achievements: list[Achievement]
    technologies: list[Skill] = Field(default_factory=list)
    date: DateRange | None = None
    # The generic `description` has been removed: according to unpacklo, a high-level
    # description without context ("image resizing tool") adds nothing that
    # well-written `achievements` do not already explain better.



class Experience(BaseModel):
    title: str
    company: str
    date: DateRange
    achievements: list[Achievement]
    is_professional: bool = True
    # Distinguishes paid professional work/studies from unpaid collaborations
    # or long-term personal projects (such as the real case
    # of "Avtrix Games", an unpaid indie studio). Useful so the renderer can,
    # if desired, indicate it transparently without the ATS penalizing it.


class Education(BaseModel):
    institution: str
    degree: str
    field: str
    achievements: ListString = Field(default_factory=ListString)
    # Kept as free text (not full Achievement objects) because Dale Kim
    # is explicit: listing subjects/courses adds no value in an entry-level
    # programmer resume. Only real accomplishments should appear here
    # (notable projects, awards), never a list of syllabus contents.


class Language(BaseModel):
    language: str
    level: str

class ProjectList(BaseModel):
    projects: list[Project] = []

class ExperienceList(BaseModel):
    experiences: list[Experience] = []

class EducationList(BaseModel):
    educations: list[Education] = []

class LanguageList(BaseModel):
    languages: list[Language] = []

class ListSkills(BaseModel):
    skills: list[Skill] = Field(default_factory=list)
