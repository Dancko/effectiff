from django.contrib import admin

from .models import User, Skill


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "name", "intro"]


admin.site.register(Skill)
