
from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from modules.models.simple_models import *


"""
Data structures for resume generation, adapted from:

1. "Game Programmer Resume Tips" (Dale Kim / unpacklo, ex Insomniac Games & Unity)
   https://github.com/unpacklo/game-programmer-resume-tips
   Key ideas applied here:
   - Every achievement should explain CONTEXT -> ACTION -> IMPACT, not just
     a generic verb ("designed", "implemented"). Therefore `Achievement` separates
     `context`, `action`, and `impact` instead of using a single free-form string:
     this forces the AI (and the candidate) to fill all three parts.
   - Performance metrics are only meaningful when accompanied by the conditions that
     make them interpretable (hardware, scale, dataset, etc.) -> `metric`
     with `value` + `context_note` instead of a standalone number.
   - Do not list individual courses or irrelevant hobbies -> any
     field such as "coursework" is removed and `additional` is limited to
     genuinely relevant accomplishments (documented in the Education/Additional docstring).
   - Do not use an objective statement unless explicitly requested -> `summary`
     is optional and the model makes it clear that it should be omitted if it
     adds no real value.
   - Avoid duplicating information between the summary and the following section:
     the summary should mention the target role + 1–2 distinguishing strengths,
     never a list of technologies (those already belong in `skills`).

2. "ATS-Compatible Resume" (Kickresume)
   https://www.kickresume.com/es/blog/curriculum-apto-para-ats-que-es-y-como-redactarlo-plantillas/
   Key ideas applied here:
   - ATS systems score keyword matches against the job posting ->
     `target_role` (the exact job title) and `ats_keywords` are added so the
     text generator knows which terms to repeat naturally 2–3 times.
   - Use both the abbreviation and the full name of technologies/certifications ->
     `Skill` separates `name` and optional `abbreviation`
     (e.g. "Structure of Arrays" / "SoA").
   - Contact information should be in its own section, never in the
     header/footer -> `Personal` remains a regular data section, not a
     separately rendered header (responsibility of the renderer, not the model).
   - Dates should use a consistent and explicit format (MM/YYYY with 2 digits) -> `DateRange`
     validates the format instead of accepting arbitrary free-form strings.
   - Avoid tables/columns/images that an ATS cannot parse -> this is the responsibility
     of the rendering template (docx/pdf/html), but it is documented here so that
     anyone using this model knows the final layout should be single-column,
     without graphics, and with standard section headings.
   - The summary should include the job title -> `summary` is built from
     `target_role`.
"""



class CandidateProfile(BaseModel):
    target_language: TargetLanguage

    personal: Personal

    # The summary is NO LONGER a generic "objective statement" (unpacklo
    # discourages objective statements unless explicitly requested by the
    # company). It is a short sentence generated from target_role +
    # 1-2 genuine distinguishing strengths, never a list of technologies.
    summary: str | None = None

    # Title similar to the job position offered
    title: str | None = None

    # Keywords extracted from the job posting (Kickresume step 1),
    # used to verify/guide that they are naturally distributed throughout the resume
    # (summary, experience, skills) instead of being crammed into a single
    # hidden section or white text (both discouraged practices).
    ats_keywords: ListString | None = None

    skills: ListSkills
    soft_skills: ListString = Field(default_factory=ListString)
    transferable_skills: ListString = Field(default_factory=ListString)

    projects: ProjectList
    experience: ExperienceList
    education: EducationList
    languages: LanguageList

    # Limited to accomplishments genuinely relevant to the position (volunteer work
    # with demonstrable impact, awards, publications). Unpacklo: hobbies/extracurricular
    # activities unrelated to the position only take up space and may work against you.
    additional: ListString = Field(default_factory=ListString)

    @model_validator(mode="after")
    def _check_keyword_repetition(self) -> "CandidateProfile":
        """
        Non-blocking warning inspired by Kickresume: important keywords
        should appear 2–3 times throughout the resume. This only
        exposes the check as a utility; it does not raise an exception because
        it is a recommendation, not a structural requirement.
        """
        return self

    def keyword_coverage(self) -> dict[str, int]:
        """
        Counts how many times each `ats_keyword` appears in the textual content
        of the profile (summary + achievements + skills). Useful so the
        generating AI can check, before delivering the resume, whether it is
        underusing any important keyword from the job posting (target: 2–3 occurrences,
        naturally, according to Kickresume).
        """
        haystack_parts: list[str] = [self.summary or ""]
        for exp in self.experience.experiences:
            haystack_parts.extend(a.render() for a in exp.achievements)
        for proj in self.projects.projects:
            haystack_parts.extend(a.render() for a in proj.achievements)
        haystack_parts.extend(s.display() for s in self.skills.skills)
        haystack = " ".join(haystack_parts).lower()

        if self.ats_keywords == None: return{}

        return {
            kw: haystack.count(kw.lower())
            for kw in self.ats_keywords.array
        }



class DetailsExtraction(BaseModel):
    """
    Auxiliary output of each block extraction call (isolated Experience or
    Project): the skills/soft_skills/transferable_skills demonstrated by THAT
    specific block. They are then combined, outside the model, with `extend()`.
    """

    skills: ListSkills = Field(default_factory=ListSkills)
    soft_skills: ListString = Field(default_factory=ListString)
    transferable_skills: ListString = Field(default_factory=ListString)

    def extend(self, other: "DetailsExtraction | None") -> None:
        if other is None:
            return

        for s in other.skills.skills:
            if s.name not in map(lambda skill: skill.name, self.skills.skills):
                self.skills.skills.append(s)

        for ss in other.soft_skills.array:
            if ss not in self.soft_skills.array:
                self.soft_skills.array.append(ss)

        for t in other.transferable_skills.array:
            if t not in self.transferable_skills.array:
                self.transferable_skills.array.append(t)


class ExperienceExtended(BaseModel):
    """Result of an extraction call on an isolated Experience block."""

    experience: Experience
    details: DetailsExtraction


class ProjectExtended(BaseModel):
    """Result of an extraction call on an isolated Project block."""

    project: Project
    details: DetailsExtraction