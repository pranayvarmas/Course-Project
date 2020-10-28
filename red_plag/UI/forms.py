#-*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 100)
    password = forms.CharField(widget = forms.PasswordInput())
    last_name=forms.CharField(max_length=100)
    passcode=forms.IntegerField(max_value=999999)
class NewUserForm(UserCreationForm):
    first_name=forms.CharField(max_length=100)
    first_name=""
    last_name=forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "first_name", "last_name")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
class ProfileForm(forms.Form):
    #name = forms.CharField(max_length = 50)
    picture = forms.FileField()
class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields["level"].choices = ( ('admin', 'administrator' ))

    class Meta:
        #model = UserProfile
        exclude = ('user',)
#class passcod(forms.Form):
 #   passcode=forms.IntegerField(max_value=999999)
class SignForm(forms.Form):
    username = forms.CharField(max_length = 100)
#    password = forms.CharField(widget = forms.PasswordInput())
    password2=forms.CharField(widget=forms.PasswordInput())
    last_name=forms.CharField(max_length=100)
    passcode=forms.IntegerField(max_value=999999)
