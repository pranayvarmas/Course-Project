#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    #user = models.OneToOneField(User)
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput())
    university=forms.CharField(max_length=100)
    passcode=forms.IntegerField(max_value=999999)
class NewUserForm(UserCreationForm):
    #first_name=forms.CharField(max_length=100)
    #first_name=""
    university=forms.CharField(max_length=100)
    email=forms.EmailField(max_length=100)
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2", "university")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
class ProfileForm(forms.Form):
    #name = forms.CharField(max_length = 50)
    picture = forms.FileField()
    language=forms.CharField(max_length=100)
    format1 = forms.CharField(max_length=100)
#class UserProfileForm(forms.ModelForm):
 #   def __init__(self, *args, **kwargs):
  #      super(UserProfileForm, self).__init__(*args, **kwargs)  
   #     self.fields["level"].choices = ( ('admin', 'administrator' ))

    #class Meta:
        #model = UserProfile
     #   exclude = ('user',)
#class passcod(forms.Form):
 #   passcode=forms.IntegerField(max_value=999999)
class SignForm(forms.Form):
    email=forms.EmailField(max_length=100)
    username = forms.CharField(max_length = 100)
    password1 = forms.CharField(max_length=100)
    password2=forms.CharField(max_length=100)
    university=forms.CharField(max_length=100)
    passcode=forms.IntegerField(max_value=999999)
class PasswordResetForm(forms.Form):
    #username=forms.CharField(max_length=100)
    #university=forms.CharField(max_length=100)
    email=forms.EmailField(max_length=100)
class PasscodeForm(forms.Form):
    passcode0=forms.IntegerField(max_value=999999)
    passcode1=forms.IntegerField(max_value=999999)
    passcode2=forms.IntegerField(max_value=999999)