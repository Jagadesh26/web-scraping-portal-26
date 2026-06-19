from apps.resumes.models import (
    ResumeProject
)

from apps.resumes.services.skill_extractor_service import (
    SkillExtractorService
)


class ProjectExtractorService:

    PROJECT_HEADERS = [
        "projects",
        "project",
        "personal projects",
        "academic projects",
        "key projects",
        "project experience",
        "work experience",
    ]

    SECTION_HEADERS = [
        "education",
        "experience",
        "work experience",
        "skills",
        "technical skills",
        "certifications",
        "achievements",
        "languages",
        "interests",
        "summary",
        "profile",
    ]

    @classmethod
    def extract_projects(
        cls,
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        lines = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

        project_section = (
            cls._extract_project_section(
                lines
            )
        )

        if not project_section:
            return []

        projects = []

        current_title = None
        current_description = []

        for line in project_section:

            if cls._is_project_title(
                line
            ):

                if current_title:

                    project = (
                        cls._save_project(
                            resume,
                            current_title,
                            current_description
                        )
                    )

                    if project:
                        projects.append(
                            project
                        )

                current_title = line

                current_description = []

            else:

                current_description.append(
                    line
                )

        if current_title:

            project = (
                cls._save_project(
                    resume,
                    current_title,
                    current_description
                )
            )

            if project:
                projects.append(
                    project
                )

        return projects

    @classmethod
    def _extract_project_section(
        cls,
        lines
    ):

        start_index = None

        for index, line in enumerate(lines):

            if (
                line.lower().strip()
                in cls.PROJECT_HEADERS
            ):

                start_index = (
                    index + 1
                )

                break

        if start_index is None:
            return []

        project_lines = []

        for line in lines[start_index:]:

            lower_line = (
                line.lower().strip()
            )

            if (
                lower_line
                in cls.SECTION_HEADERS
            ):

                break

            project_lines.append(
                line
            )

        return project_lines

    @classmethod
    def _is_project_title(
        cls,
        line
    ):

        if not line:
            return False

        if len(line) > 60:
            return False

        if line.endswith("."):
            return False

        if len(line.split()) > 8:
            return False

        words = line.split()

        capitalized_words = sum(
            1
            for word in words
            if word[:1].isupper()
        )

        if (
            capitalized_words
            >= max(
                1,
                len(words) // 2
            )
        ):
            return True

        return False

    @classmethod
    def _save_project(
        cls,
        resume,
        title,
        description_lines
    ):

        description = "\n".join(
            description_lines
        ).strip()

        technologies = (
            SkillExtractorService
            .extract_skills_from_text(
                description
            )
        )

        return ResumeProject.objects.create(
            resume=resume,
            project_name=title,
            description=description,
            technologies=", ".join(
                technologies
            )
        )