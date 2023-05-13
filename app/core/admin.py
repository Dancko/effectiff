from django.contrib import admin

from .models import User, Task, Category, Project

admin.site.register(User)
admin.site.register(Task)
admin.site.register(Category)
admin.site.register(Project)
