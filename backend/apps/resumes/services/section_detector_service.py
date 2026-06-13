
class SectionDetectorService:

    SECTION_HEADERS = {
        "skills": [
            "skills",
            "technical skills",
            "core skills",
            "key skills",
            "technical expertise",
            "competencies",
            "areas of expertise",
            "skills and expertise",
            "skills summary",
            "skills overview",
            "skills set",
            "skills profile",
        ],

        "experience": [
            "experience",
            "work experience",
            "professional experience",
            "employment history",
            "career history",
            "work history",
            "relevant experience",
            "experience summary",
            "experience overview",
            "experience details",
            "experience profile",
            "experience highlights",
        ],

        "education": [
            "education",
            "academic background",
            "academic qualifications",
            "qualification",
            "educational qualifications",
            "educational background",
            "education and qualifications",
            "education details",
            "education overview",
            "education profile",
            "education highlights",
        ],

        "projects": [
            "projects",
            "project experience",
            "academic projects",
            "professional projects",
            "personal projects",
            "project details",
            "project overview",
            "project profile",
            "project highlights",
            "project summary",
            "project description",
        ]
    }




    @classmethod
    def detect_sections(
        cls,
        raw_text
    ):

        text = raw_text.lower()

        sections = {
            "skills": "",
            "experience": "",
            "education": "",
            "projects": "",
        }

        lines = raw_text.splitlines()

        current_section = None

        for line in lines:

            cleaned_line = line.strip().lower()

            found = False

            for section_name, aliases in (
                cls.SECTION_HEADERS.items()
            ):

                if cleaned_line in aliases:

                    current_section = section_name

                    found = True

                    break

            if found:
                continue

            if current_section:

                sections[current_section] += (
                    line + "\n"
                )

        return sections