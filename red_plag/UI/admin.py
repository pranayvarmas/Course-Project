from django.contrib import admin
from .models import UserModel

class UniversityAdmin(admin.ModelAdmin):
   list_display = ('username', 'university')

admin.site.register(UserModel, UniversityAdmin)

