# Copyright (c) 2013 Ankur Sethi <contact@ankursethi.in>
# Licensed under the terms of the MIT license.
# See the file LICENSE for copying permissions.


from django.contrib import admin
from tracker import models

admin.site.register(models.ApiToken)
admin.site.register(models.Project)
admin.site.register(models.Task)
admin.site.register(models.WorkSession)
