import re

from apps.resumes.models import (
    ResumeEducation
)


class EducationExtractorService:

    DEGREE_PATTERNS = [
        "b.tech",
        "b.e",
        "bsc",
        "b.sc",
        "bca",
        "m.tech",
        "m.e",
        "msc",
        "m.sc",
        "mca",
        "phd",
        "bachelor",
        "master",
    ]

    @classmethod
    def extract_education(
        cls,
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        educations = []

        lines = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

        current_degree = None
        current_institution = None
        start_year = None
        end_year = None

        year_pattern = r"(19|20)\d{2}"

        for line in lines:

            lower_line = line.lower()

            if any(
                degree in lower_line
                for degree in cls.DEGREE_PATTERNS
            ):

                current_degree = line

                continue

            years = re.findall(
                year_pattern,
                line
            )

            if years:

                extracted_years = re.findall(
                    r"(?:19|20)\d{2}",
                    line
                )

                if len(extracted_years) >= 2:

                    start_year = int(
                        extracted_years[0]
                    )

                    end_year = int(
                        extracted_years[1]
                    )

                continue

            if current_degree and not current_institution:

                current_institution = line

                education = (
                    ResumeEducation.objects.create(
                        resume=resume,
                        degree=current_degree,
                        institution=current_institution,
                        start_year=start_year,
                        end_year=end_year
                    )
                )

                educations.append(
                    education
                )

                current_degree = None
                current_institution = None
                start_year = None
                end_year = None

        return educations