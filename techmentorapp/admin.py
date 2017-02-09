from django.contrib import admin
from .models import Profile, Mentor, Skill, Skill_Detail, Review, Reserve, Available, Infomation

# Register your models here.
admin.site.register(Profile)


class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'about', '_skill', 'status', 'user', 'update_time', 'create_time')

    def _skill(self, row):
        return ','.join([x.name for x in row.skill.all()])



admin.site.register(Mentor, SkillAdmin)
admin.site.register(Skill)
admin.site.register(Review)
admin.site.register(Reserve)
admin.site.register(Available)
admin.site.register(Infomation)

admin.site.register(Skill_Detail)