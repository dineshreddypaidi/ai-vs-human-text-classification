from django.contrib import admin
from . import models

# Register your models here.

class Admin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    
admin.site.register(models.UserProfile, Admin)
admin.site.register(models.History, Admin)