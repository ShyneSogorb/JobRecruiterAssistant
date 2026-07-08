from pydantic import BaseModel

class Personal(BaseModel):
    name: str
    role: str
    location: str
    email: str
    phone: str
    website: str
    linkedin: str
    github: str

class Project(BaseModel):
    name: str
    description: str
    achievements: list[str]
    technologies: list[str]

class DateRange(BaseModel):
    start: str
    end: str

class Experience(BaseModel):
    title: str
    company: str
    date: DateRange
    achievements: list[str]

class Education(BaseModel):
    institution: str
    degree: str
    field: str
    achievements: list[str]

class Language(BaseModel):
    language: str
    level: str


class CandidateProfile(BaseModel):
    language: str

    personal: Personal

    summary: str

    skills: list[str]

    projects: list[Project]
    experience: list[Experience]
    education: list[Education]
    languages: list[Language]

    additional: list[str]