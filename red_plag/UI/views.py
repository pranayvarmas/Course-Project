from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .forms import NewUserForm
from UI.forms import ProfileForm,SignForm
from UI.models import Profile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
# Create your views here.
#-*- coding: utf-8 -*-
from UI.forms import LoginForm
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from numpy import array
#@login_required(login_url='/')
#from django.template.defaulttags import csrf_token
#from django.template import RequestContext
#@csrf_token
def login1(request):
	username=None
	if request.user.is_authenticated:
		username = request.user.username
		return render(request, 'loggedin.html', {"username":username})
	else:
		if request.method=="POST":
			#print(request.POST)
      #Get the posted form
			MyLoginForm = LoginForm(request.POST)
			if MyLoginForm.is_valid():
				username = MyLoginForm.cleaned_data['username']
				password=MyLoginForm.cleaned_data['password']
				last_name=MyLoginForm.cleaned_data['last_name']
				passcode=MyLoginForm.cleaned_data['passcode']
				temp=test(request,last_name, passcode)
				if temp:
					user=authenticate(username=username, password=password)
					if user is not None:
						login(request, user)
						sec=request.user
						if (sec.last_name==last_name):
							return render(request, 'loggedin.html', {"username":username})
						else:
							logout(request)
							message1="Invalid Organization match"
							return render(request, 'login.html', {"message1":message1})
					else:
						message1="Username or Password is Incorrect"
#						message1="Invalid username or password."
						return render(request,'login.html', {"message1":message1} )
				else:
					message1="Invalid Passcode"
					return render(request, 'login.html', {"message1":message1})
			else:
				print(MyLoginForm.errors)
				message1="All fields are mandatory"
#				message1=message2
#				message1.replace('<ul', '')
#				message1.replace('class="errorlist"', '')
#				message1.replace('li', '')
#				message1.replace('<', '')
#				message1.replace('>', '')
#				message1.replace('{', '')
#				print(MyLoginForm.non_field_errors)
#				print("1")
#				error="Invalid username or password."
				return render(request,'login.html', {"message1":message1} )
			form = LoginForm()
			return render(request,'loggedin.html', {"username":username})
		else:
			return render(request, 'login.html')

#	return render(request, 'loggedin.html', {"username" : username})
def signup(request):
	if request.user.is_authenticated:
		return render(request, 'error.html')
	else:
		return render(request, 'signup.html')
def save(request):
	if request.method == 'POST':
		form1 = NewUserForm(request.POST)
		form2 = SignForm(request.POST)
#		print(request.POST)
#		print(form1)
		if (form1.is_valid() and form2.is_valid()):
#			print("yes")
#			sec=form1.last_name
#			sec.last_name=sec.last_name+form1.cleaned_data["organization"]
#			passcode=form1.cleaned_data["passcode"]
			temp=test(request,form2.cleaned_data['last_name'], form2.cleaned_data['passcode'])
			if temp:
#				print(1)
				form1.save()
				message1="Account Created Succesfully"
				return render(request, 'login.html', {"message1":message1})
			else:
				message1="Invalid Organization Passcode"
				return render(request, 'signup.html', {"message1":message1})
		else:
			#message1=form1.errors
			message2=form2.errors
			return render(request,'signup.html', {"message2":message2} )
	form1 = UserCreationForm()
	message1="Invalid"
#	print ("hai")
	return render(request, "login.html", {"message1":message1})
def loggedin(request):
	saved = False
	username=None
	if request.user.is_authenticated:
		username = request.user.username
		if request.method == "POST":
      #Get the posted form
			MyProfileForm = ProfileForm(request.POST, request.FILES)

			if MyProfileForm.is_valid():
				profile = Profile()
				#profile.name = MyProfileForm.cleaned_data["name"]
				profile.picture = MyProfileForm.cleaned_data["picture"]
				profile.save()
				saved = True
				i=Profile.objects.all().count()-1
				i=i+1
#				print(i)
				first=request.user
				first.first_name=first.first_name+str(i)+";"
				first.save()
				message1="Successfully Uploaded"
			else:
				message1="No file Uploaded"
#				print(MyProfileForm.errors)

				return render(request, 'loggedin.html', {"message1":message1, "username":username})
		else:
			MyProfileForm = Profileform()
		return render(request, 'loggedin.html', {"message1":message1, "username":username} )
	else:
		return render(request, 'login.html')
def logoutin(request):
	username=None
	if request.user.is_authenticated:
		username = request.user.username
		logout(request)
		message1="Logged Out Succesfully"
		return render(request, 'login.html', {"message1":message1})
	else:
		return render(request, 'login.html')

def change(request):
	username=None
	if request.user.is_authenticated:
		username = request.user.username
		message1=""
		return render(request, 'change.html', {"message1":message1})
	else:
		return render(request, 'login.html')
def password(request):
	username=None
	if request.user.is_authenticated:
		username=request.user.username
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)  # Important!
				message1="Your password has successfully updated!"
				return render(request, 'loggedin.html', {"username":username, "message1":message1})

			else:
				message1="Error Messages:"
				message2=form.errors
				return render(request, 'change.html', {"message1":message1, "message2":message2})
		else:
			form = PasswordChangeForm(request.user)
		message1=""
		return render(request, 'login.html', {"message1":message1})
	else:
		return render(request, 'login.html')
def loghome(request):
	username=None
	if request.user.is_authenticated:
		username = request.user.username
		message1=""
		return render(request, 'loggedin.html', {"message1":message1, "username":username})
	else:
		return render(request, 'login.html')
def temporary(request, temp):
	username=None
	message1=""
	if request.user.is_authenticated:
		username = request.user.username
		return render(request, 'loggedin.html', {"message1":message1, "username":username})
	else:
		return render(request, 'login.html')

def yourfiles(request):
	if request.user.is_authenticated:
		#context = Identity_unique.objects.filter(user=request.user)
		s=request.user.first_name
		#s="1;2;3;4;5;6;7;8;9;0;10;11;12;13;14;15;16;17;18;19;20;"
		t=s.split(";")
#		print(t)
			#file[e]=(Profile.objects.filter(id=int(row)))
			#e=e+1
		context = {'file': Profile.objects.filter(id__in=t[:-1])}
#		print(context)
		return render(request, 'yourfiles.html', context);
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1})

def download(request, path):
	if request.user.is_authenticated:
		file_path = os.path.join(settings.MEDIA_ROOT, path)
		if os.path.exists(file_path):
			with open(file_path, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/py")
				response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
				return response
		raise Http404
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1})
def orga(request):
	if request.user.is_authenticated:
		username=request.user.username
		return render(request, 'organization.html', {"username":username})
	else:
		message1="Please login to enter Organization Passcode"
		return render(request, 'login.html', {"message1":message1})
def org(request):
	if request.user.is_authenticated:
		username=request.user.username
		if request.method=="POST":
			form=passcod(request.POST)
			if form.is_valid():
				passcode=form.cleaned_data["passcode"]
				if(passcode==123456):
					return render(request, 'loggedin.html', {"username":username})
				else:
					message1="Organization Passcode is incorrect"
					return render(request, 'organization.html', {"username":username, "message1":message1})
			else:
#				print(form.errors)
				message1="Organization Passcode is Invalid"
				return render(request, 'organization.html', {"username":username, "message1":message1})
		else:
			form=passcod()
			message1="Organization Passcode is Invalid"
			logoutin(request)
			return render(request, 'login.html', {"message1":message1})
	else:
		message1="Please login to enter Organization Passcode"
		return render(request, 'login.html', {"message1":message1})
def test(request, last_name, passcode):
	org=last_name
	if (org=="IIT Bombay"):
		if (passcode==123456):
			return True
		else:
			return False
	else:
		if (org=="IIT Madras"):
			if (passcode==111111):
				return True
			else:
				return False

