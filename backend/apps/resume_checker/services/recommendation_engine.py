class ResumeRecommendationEngine:

    @staticmethod
    def unique(
        values
    ):
        seen = set()
        result = []

        for value in values:
            if value and value not in seen:
                seen.add(
                    value
                )
                result.append(
                    value
                )

        return result

    @classmethod
    def combine(
        cls,
        analyzer_results
    ):
        strengths = []
        weaknesses = []
        recommendations = []

        for result in analyzer_results:
            strengths.extend(
                result.get(
                    "strengths",
                    [],
                )
            )
            weaknesses.extend(
                result.get(
                    "weaknesses",
                    [],
                )
            )
            recommendations.extend(
                result.get(
                    "recommendations",
                    [],
                )
            )

        return {
            "strengths": cls.unique(
                strengths
            ),
            "weaknesses": cls.unique(
                weaknesses
            ),
            "recommendations": cls.unique(
                recommendations
            ),
        }

