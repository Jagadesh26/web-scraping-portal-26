from apps.resumes.models import (
    ResumeProject
)


class ProjectExtractorService:

    @staticmethod
    def extract_projects(
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        projects = []

        lines = [
            line.strip()
            for line in raw_text.splitlines()
            if line.strip()
        ]

        current_project = None
        description_lines = []

        for line in lines:

            if len(line) <= 80:

                if current_project:

                    project = (
                        ResumeProject.objects.create(
                            resume=resume,
                            project_name=current_project,
                            description="\n".join(
                                description_lines
                            )
                        )
                    )

                    projects.append(
                        project
                    )

                current_project = line

                description_lines = []

            else:

                description_lines.append(
                    line
                )

        if current_project:

            project = (
                ResumeProject.objects.create(
                    resume=resume,
                    project_name=current_project,
                    description="\n".join(
                        description_lines
                    )
                )
            )

            projects.append(
                project
            )

        return projects