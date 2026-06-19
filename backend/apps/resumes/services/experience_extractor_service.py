import re
from datetime import date

from apps.resumes.models import (
    ResumeExperience
)


class ExperienceExtractorService:

    DESIGNATION_WORDS = (
        "Developer",
        "Engineer",
        "Manager",
        "Analyst",
        "Consultant",
        "Specialist",
        "Administrator",
        "Architect",
        "Lead",
        "Director",
        "Trainee",
        "Intern",
        "Coordinator",
        "Designer",
        "Executive",
    )

    DATE_RANGE_PATTERN = re.compile(
        r"(?P<start>(?:19|20)\d{2}(?:[-/](?:0?[1-9]|1[0-2]))?)\s*"
        r"(?:-|–|—|to|→|->)\s*"
        r"(?P<end>present|current|(?:19|20)\d{2}(?:[-/](?:0?[1-9]|1[0-2]))?)",
        re.IGNORECASE
    )

    @staticmethod
    def parse_resume_date(value):
        value = value.strip().lower()

        if value in {"present", "current"}:
            return date.today()

        match = re.match(
            r"(?P<year>(?:19|20)\d{2})(?:[-/](?P<month>0?[1-9]|1[0-2]))?",
            value
        )

        if not match:
            return None

        return date(
            int(match.group("year")),
            int(match.group("month") or 1),
            1
        )

    @staticmethod
    def calculate_years(start_date, end_date):
        if not start_date:
            return 0

        end_date = end_date or date.today()
        days = max(
            (
                end_date - start_date
            ).days,
            0
        )

        return round(
            days / 365,
            2
        )

    @classmethod
    def looks_like_designation(cls, line):
        lower_line = line.lower()

        return any(
            word.lower() in lower_line
            for word in cls.DESIGNATION_WORDS
        )

    @staticmethod
    def extract_experience(
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        experiences = []

        lines = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

        used_keys = set()

        for index, line in enumerate(lines):
            date_match = ExperienceExtractorService.DATE_RANGE_PATTERN.search(
                line
            )

            if not date_match:
                continue

            start_date = ExperienceExtractorService.parse_resume_date(
                date_match.group("start")
            )
            end_date = ExperienceExtractorService.parse_resume_date(
                date_match.group("end")
            )

            context = lines[
                max(
                    index - 2,
                    0
                ): index + 1
            ]
            designation = ""
            company_name = ""

            for context_line in reversed(context):
                cleaned = ExperienceExtractorService.DATE_RANGE_PATTERN.sub(
                    "",
                    context_line
                ).strip(" -|,")

                if not cleaned:
                    continue

                if not designation and ExperienceExtractorService.looks_like_designation(
                    cleaned
                ):
                    designation = cleaned
                    continue

                if not company_name:
                    company_name = cleaned

            if not designation:
                designation = "Not specified"

            if not company_name:
                company_name = "Not specified"

            key = (
                company_name.lower(),
                designation.lower(),
                start_date,
                end_date,
            )

            if key in used_keys:
                continue

            used_keys.add(
                key
            )

            experience = ResumeExperience.objects.create(
                resume=resume,
                company_name=company_name,
                designation=designation,
                start_date=start_date,
                end_date=end_date,
                years_of_experience=ExperienceExtractorService.calculate_years(
                    start_date,
                    end_date
                ),
                description=""
            )

            experiences.append(
                experience
            )

        return experiences
