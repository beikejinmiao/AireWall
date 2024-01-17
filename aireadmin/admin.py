from django.contrib import admin
from aireadmin import models

admin.site.register(models.User)
admin.site.register(models.APIKey)

