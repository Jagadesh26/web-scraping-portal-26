from apps.resume_checker.services.base import AnalyzerBase


class ResumeProjectsAnalyzer(AnalyzerBase):

    @classmethod
    def analyze(
        cls,
        resume
    ):
        projects = list(
            resume.projects.all()
        )

        score = 0
        strengths = []
        weaknesses = []
        recommendations = []

        if len(
            projects
        ) >= 3:
            score += 35
            strengths.append(
                "Strong project count."
            )
        elif len(
            projects
        ) >= 1:
            score += 22
            strengths.append(
                "Project experience is present."
            )
        else:
            weaknesses.append(
                "Projects are missing."
            )
            recommendations.append(
                "Add at least two projects with problem, technology, and result."
            )

        detailed_projects = 0
        technology_projects = 0

        for project in projects:
            description = cls.normalize_text(
                project.description
            )
            technologies = cls.normalize_text(
                project.technologies
            )
            combined = f"{description} {technologies}"

            if len(
                description
            ) >= 80:
                detailed_projects += 1

            if len(
                cls.tokenize(
                    combined
                )
            ) >= 3:
                technology_projects += 1

        if projects and detailed_projects == len(
            projects
        ):
            score += 35
            strengths.append(
                "Project descriptions are detailed."
            )
        elif detailed_projects:
            score += 20
            recommendations.append(
                "Add more detail to shorter project descriptions."
            )
        elif projects:
            score += 8
            weaknesses.append(
                "Project descriptions are too short."
            )
            recommendations.append(
                "Explain what each project does, which stack you used, and what you delivered."
            )

        if projects and technology_projects == len(
            projects
        ):
            score += 30
            strengths.append(
                "Project technologies are clearly mentioned."
            )
        elif technology_projects:
            score += 18
            recommendations.append(
                "Mention the technologies used for every project."
            )
        elif projects:
            weaknesses.append(
                "Project technologies are missing."
            )
            recommendations.append(
                "Add technology keywords such as Django, PostgreSQL, Docker, or AWS to project details."
            )

        return {
            "score": cls.clamp_score(
                score
            ),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }

