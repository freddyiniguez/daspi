from django.contrib import admin
from .models import Project, Estimate, Task

admin.site.register(Project)
admin.site.register(Estimate)
admin.site.register(Task)
