from django.contrib import admin
from .models import UserModel, UniversityModel

class UserAdmin(admin.ModelAdmin):
   list_display = ('username', 'university', 'email')
class UniversityAdmin(admin.ModelAdmin):
	list_display = ('username', 'university', 'email')
admin.site.register(UserModel, UserAdmin)
admin.site.register(UniversityModel, UniversityAdmin)

