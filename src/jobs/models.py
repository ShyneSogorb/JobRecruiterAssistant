from pydantic import BaseModel
from enum import Flag

class Salary(BaseModel):
    currency: str | None = None
    minimum: float | None = None
    maximum: float | None = None
    period: str | None = None   # hour, month, year

def get_active_flags_name(flag: Flag) -> str:
    return "|".join(f.name for f in flag)

#use bitflag-like in case of multiple options
class JobModality(Flag):
    unknown = 0
    onsite = 1
    hybrid = 2
    remote = 4

    def __str__(self) -> str:
        return get_active_flags_name(self)

#use bitflag-like in case of multiple options
class EmploymentType(Flag):
    unknown = 0
    full_time = 1
    part_time = 2
    contract = 4
    internship = 8
    freelance = 16
    temporary = 32

    def __str__(self) -> str:
        return get_active_flags_name(self)
    
class ExperienceLevel(Flag):
    unknown = 0
    intern = 1
    junior = 2
    mid = 4
    senior = 8
    lead = 16
    
    def __str__(self) -> str:
        return get_active_flags_name(self)

class LanguageRequirement(BaseModel):
    language: str
    level: str | None = None


class JobOffer(BaseModel):
    company: str
    title: str
    location: str
    url: str | None = None

    work_mode: JobModality

    employment_type: EmploymentType

    description: str

    required_skills: list[str]
    preferred_skills: list[str]

    languages: list[LanguageRequirement]

    salary: Salary | None = None