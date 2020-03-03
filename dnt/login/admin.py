from django.contrib import admin
from . import models
# Used for backend /admin
admin.site.register(models.User)
admin.site.register(models.ConfirmString) 
admin.site.register(models.PasswordString) 
