from django.contrib import admin
from tracker import models

admin.site.register(models.ApiToken)
admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.WorkSession)
