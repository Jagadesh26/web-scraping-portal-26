from django.contrib import admin

from apps.resumes.models import (
    Resume,
    ResumeAnalysis,
    ResumeEducation,
    ResumeExperience,
    ResumeProject,
    ResumeRecommendation,
    ResumeSkill,
    Skill,
)


admin.site.register(Resume)
admin.site.register(ResumeAnalysis)
admin.site.register(ResumeEducation)
admin.site.register(ResumeExperience)
admin.site.register(ResumeProject)
admin.site.register(ResumeRecommendation)
admin.site.register(ResumeSkill)
admin.site.register(Skill)
