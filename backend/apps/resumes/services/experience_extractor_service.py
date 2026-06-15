import re

from apps.resumes.models import (
    ResumeExperience
)


class ExperienceExtractorService:

    @staticmethod
    def extract_experience(
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        experiences = []

        pattern = (
            r"([A-Za-z ]+)\s+"
            r"(Developer|Engineer|Manager|Analyst|Consultant|Specialist|Administrator|Architect|Lead|Head|Director|Trainee|Intern|Coordinator|Supervisor|Technician|Designer|Strategist|Planner|Officer|Executive|Assistant|Representative|Advisor|Trainer|Instructor|Facilitator|Counselor|Coach|Mentor)\b"
        )

        matches = re.findall(
            pattern,
            raw_text,
            re.IGNORECASE
        )

        for company, designation in matches:

            experience = (
                ResumeExperience.objects.create(
                    resume=resume,
                    company_name=company.strip(),
                    designation=designation.strip(),
                    description=""
                )
            )

            experiences.append(
                experience
            )

        return experiences
