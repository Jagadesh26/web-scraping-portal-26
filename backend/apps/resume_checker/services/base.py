import re


class AnalyzerBase:

    @staticmethod
    def clamp_score(score):
        return max(
            0,
            min(
                100,
                round(
                    score,
                    2,
                ),
            ),
        )

    @staticmethod
    def normalize_text(value):
        return (
            value
            or ""
        ).strip()

    @staticmethod
    def tokenize(value):
        return {
            item.lower()
            for item in re.findall(
                r"[a-zA-Z][a-zA-Z0-9+#./-]*",
                value or "",
            )
        }

    @staticmethod
    def has_number(value):
        return bool(
            re.search(
                r"\d",
                value or "",
            )
        )

