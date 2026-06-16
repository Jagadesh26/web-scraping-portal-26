from apps.resumes.models import Resume


class ResumeStructureAnalyzer:

    @staticmethod
    def analyze(
        resume
    ):

        if not isinstance(
            resume,
            Resume
        ):

            return {
                "score": 0,
                "strengths": [],
                "weaknesses": [
                    "Resume not found."
                ],
                "recommendations": [
                    "Upload and parse your resume before running ATS analysis."
                ],
            }

        score = 0

        strengths = []

        weaknesses = []

        recommendations = []

        if resume.skills.exists():

            score += 25
            strengths.append(
                "Skills section detected."
            )

        else:

            weaknesses.append(
                "Skills section is missing."
            )
            recommendations.append(
                "Add a skills section."
            )

        if resume.experiences.exists():

            score += 25
            strengths.append(
                "Experience section detected."
            )

        else:

            weaknesses.append(
                "Experience section is missing."
            )
            recommendations.append(
                "Add an experience section."
            )

        if resume.educations.exists():

            score += 25
            strengths.append(
                "Education section detected."
            )

        else:

            weaknesses.append(
                "Education section is missing."
            )
            recommendations.append(
                "Add an education section."
            )

        if resume.projects.exists():

            score += 25
            strengths.append(
                "Projects section detected."
            )

        else:

            weaknesses.append(
                "Projects section is missing."
            )
            recommendations.append(
                "Add a projects section."
            )

        return {

            "score": score,

            "strengths": strengths,

            "weaknesses": weaknesses,

            "recommendations": recommendations,
        }
