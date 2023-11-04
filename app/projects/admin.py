from django.contrib import admin

from .models import Project, Category


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]


admin.site.register(Category)
