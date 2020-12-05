from django.db import models
from django.contrib.auth.models import Group, User
import os
from django import forms
#new_group, created = Group.objects.get_or_create(name=group_name)
class Profile(models.Model):
   #name = models.CharField(max_length = 50)
    picture = models.FileField(upload_to = '')
    def name(self):
        return os.path.basename(self.picture.name)

    class Meta:
      db_table = "profile"
      
class UserModel(models.Model):
   username = models.CharField(max_length=100)
   #password=forms.CharField(max_length=100)
   email=models.EmailField(max_length=100, default="temp@user.com")
   university = models.CharField(max_length=100)
   uploads=models.CharField(max_length=100, default="")
   last_login=models.DateTimeField(auto_now=True)
   passcode=models.IntegerField(default=000000)
   def __str__(self):
      return self.username
   
   class Meta:
      db_table = "usersinfo"
class UniversityModel(models.Model):
  username = models.CharField(max_length=100)
  university = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, default="temp@univ.con")
  uploads = models.CharField(max_length=100, default="-1")
  last_login = models.DateTimeField(auto_now=True)
  passcode = models.IntegerField(default=000000)
  def __str__(self):
      return self.username
   
  class Meta:
      db_table = "univsinfo"

