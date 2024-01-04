from django.contrib import admin

from .models import Project, ProjectFile, Category


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["title", "owner"]


admin.site.register(Category)
admin.site.register(ProjectFile)
