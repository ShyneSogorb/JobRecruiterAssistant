from __future__ import annotations

from typing import Any

import pandas as pd

from modules.models.job_models import (
    EmploymentType,
    ExperienceLevel,
    JobModality,
    JobOffer,
    LanguageRequirement,
    Salary,
    SalaryCurrency,
    SalaryPeriod,
    TargetLanguage,
)


class JobSpyParser:

    @staticmethod
    def parse(df: pd.DataFrame) -> list[JobOffer]:
        return [
            JobSpyParser._parse_row(row)
            for _, row in df.iterrows()
        ]

    @staticmethod
    def _parse_row(row: pd.Series) -> JobOffer:
        return JobOffer(
            id = JobSpyParser._str(row.id),
            company=JobSpyParser._str(row.company),
            role=JobSpyParser._str(row.title),
            location=JobSpyParser._str(row.location),
            url=JobSpyParser._first_non_empty(
                row.job_url_direct,
                row.job_url,
            ),
            target_language=TargetLanguage.English,

            work_mode=JobSpyParser._parse_work_mode(row),

            employment_type=JobSpyParser._parse_employment_type(row),

            experience_level=JobSpyParser._parse_experience_level(row),

            description=JobSpyParser._str(row.description),

            required_skills=[],
            preferred_skills=[],
            languages=[],

            salary=JobSpyParser._parse_salary(row),
        )

    @staticmethod
    def _parse_salary(row: pd.Series) -> Salary | None:
        if (
            pd.isna(row.min_amount)
            and pd.isna(row.max_amount)
            and pd.isna(row.currency)
        ):
            return None

        return Salary(
            currency=JobSpyParser._parse_currency(row.currency),
            minimum=None if pd.isna(row.min_amount) else float(row.min_amount),
            maximum=None if pd.isna(row.max_amount) else float(row.max_amount),
            period=JobSpyParser._parse_period(row.interval),
        )

    @staticmethod
    def _parse_currency(currency: Any):

        if pd.isna(currency):
            return None

        c = str(currency).lower()

        mapping = {
            "eur": SalaryCurrency.euros,
            "€": SalaryCurrency.euros,
            "usd": SalaryCurrency.american_dollars,
            "$": SalaryCurrency.american_dollars,
            "pln": SalaryCurrency.zloty,
            "gbp": SalaryCurrency.pounds,
            "jpy": SalaryCurrency.yen,
            "yen": SalaryCurrency.yen,
        }

        return mapping.get(c, currency)

    @staticmethod
    def _parse_period(period: Any) -> SalaryPeriod:

        if pd.isna(period):
            return SalaryPeriod.unknown

        mapping = {
            "hour": SalaryPeriod.hour,
            "month": SalaryPeriod.month,
            "year": SalaryPeriod.year,
        }

        return mapping.get(
            str(period).lower(),
            SalaryPeriod.unknown,
        )

    @staticmethod
    def _parse_work_mode(row: pd.Series) -> list[JobModality]:

        modes = []

        if bool(row.is_remote):
            modes.append(JobModality.remote)

        value = JobSpyParser._str(row.work_from_home_type).lower()

        if "hybrid" in value:
            modes.append(JobModality.hybrid)

        if "onsite" in value:
            modes.append(JobModality.onsite)

        if not modes:
            modes.append(JobModality.unknown)

        return list(dict.fromkeys(modes))

    @staticmethod
    def _parse_employment_type(row: pd.Series):

        value = JobSpyParser._str(row.job_type).lower()

        mapping = {
            "full-time": EmploymentType.full_time,
            "full time": EmploymentType.full_time,
            "part-time": EmploymentType.part_time,
            "part time": EmploymentType.part_time,
            "contract": EmploymentType.contract,
            "internship": EmploymentType.internship,
            "intern": EmploymentType.internship,
            "temporary": EmploymentType.temporary,
            "freelance": EmploymentType.freelance,
        }

        result = [
            enum
            for text, enum in mapping.items()
            if text in value
        ]

        return result or [EmploymentType.unknown]

    @staticmethod
    def _parse_experience_level(row: pd.Series):

        text = (
            JobSpyParser._str(row.job_level)
            + " "
            + JobSpyParser._str(row.experience_range)
            + " "
            + JobSpyParser._str(row.title)
        ).lower()

        if "lead" in text:
            return [ExperienceLevel.lead]

        if "senior" in text:
            return [ExperienceLevel.senior]

        if "junior" in text:
            return [ExperienceLevel.junior]

        if "intern" in text:
            return [ExperienceLevel.intern]

        if "mid" in text:
            return [ExperienceLevel.mid]

        return [ExperienceLevel.unknown]

    @staticmethod
    def _first_non_empty(*values):

        for value in values:

            if pd.isna(value):
                continue

            value = str(value).strip()

            if value:
                return value

        return ""

    @staticmethod
    def _str(value):

        if pd.isna(value):
            return ""

        return str(value)