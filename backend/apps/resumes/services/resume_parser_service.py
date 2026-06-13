from django.db import transaction

from apps.resumes.models import (
    Resume,
    ResumeAnalysis
)

from apps.resumes.parsers.parser_factory import (
    ParserFactory
)


from apps.resumes.services.section_detector_service import (
    SectionDetectorService
)

from apps.resumes.services.skill_extractor_service import (
    SkillExtractorService
)

from apps.resumes.services.experience_extractor_service import (
    ExperienceExtractorService
)



import logging

logger = logging.getLogger(__name__)


class ResumeParserService:

    @staticmethod
    @transaction.atomic
    def parse_resume(
        resume: Resume,
        file_path: str
    ):

        try:

            resume.status = "PROCESSING"
            resume.save(
                update_fields=["status"]
            )

            parser = (
                ParserFactory.get_parser(
                    resume.file_type
                )
            )

            raw_text = (
                parser.extract_text(
                    file_path
                )
            )

            analysis, created = (
                ResumeAnalysis.objects.get_or_create(
                    resume=resume
                )
            )

            analysis.raw_text = raw_text

            analysis.save()

            resume.status = "COMPLETED"

            resume.save(
                update_fields=["status"]
            )

            from apps.resumes.services.skill_extractor_service import (
                SkillExtractorService
            )

            sections = (
                SectionDetectorService.detect_sections(
                    raw_text
                )
            )

            SkillExtractorService.extract_skills(
                resume=resume,
                raw_text=sections["skills"]
            )

            ExperienceExtractorService.extract_experience(
                resume=resume,
                raw_text=sections["experience"]
            )

            EducationExtractorService.extract_education(
                resume=resume,
                raw_text=sections["education"]
            )

            ProjectExtractorService.extract_projects(
                resume=resume,
                raw_text=sections["projects"]
            )

            from apps.resumes.services.experience_extractor_service import (
                ExperienceExtractorService
            )

            ExperienceExtractorService.extract_experience(
                resume=resume,
                raw_text=raw_text
            )

            return analysis

        except Exception as exc:

            logger.exception(
                f"Resume parsing failed: {resume.id}"
            )

            resume.status = "FAILED"

            resume.save(
                update_fields=["status"]
            )

            raise