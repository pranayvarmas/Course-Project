from django.shortcuts import render
from django.shortcuts import render
from .forms import NewUserForm
from UI.forms import ProfileForm,SignForm, PasswordResetForm
from UI.models import Profile, UserModel, UserModel
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
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
from django.shortcuts import redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from django.contrib.auth.tokens import default_token_generator
import datetime
import random
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
global ran
def login1(request):
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).uploads!="-1":
			username = request.user.username
			return redirect('dashboard', username=username)
		else:
			username = request.user.username
			return redirect('univdashboard', username=username)
	else:
		if request.method=="POST":
			MyLoginForm = LoginForm(request.POST)
			if MyLoginForm.is_valid():
				username = MyLoginForm.cleaned_data['username']
				password=MyLoginForm.cleaned_data['password']
				university=MyLoginForm.cleaned_data['university']
				passcode=MyLoginForm.cleaned_data['passcode']
				user=authenticate(request, username=username, password=password)
				if user is not None:
					if UserModel.objects.get(username=username).uploads!="-1":
						temp=test(request,university, passcode)
						if temp:
							sample=UserModel.objects.get(username=username)
							#print(sample.university)
							if sample.university==university:
								login(request, user)
								sample=UserModel.objects.get(username=request.user.username)
								sample.last_login=datetime.datetime.now()
								sample.save()
								#sec=request.user
								return redirect('dashboard', username=request.user.username)
							else:
							#	logout(request)
								message1="University doesn't match"
								return render(request, 'login.html', {"message1":message1})
						else:
							message1="Invalid Passcode"
							return render(request, 'login.html', {"message1":message1})
					else:
						if UserModel.objects.get(username=username).uploads=="-1":
							temp=test(request,university, passcode)
							if temp:
								sample=UserModel.objects.get(username=username)
								#print(sample.university)
								if sample.university==university:
									login(request, user)
									sample=UserModel.objects.get(username=request.user.username)
									sample.last_login=datetime.datetime.now()
									sample.save()
									#sec=request.user
									return redirect('univdashboard', username=request.user.username)
								else:
							#		logout(request)
									message1="University doesn't match"
									return render(request, 'login.html', {"message1":message1})
							else:
								message1="Invalid Passcode"
								return render(request, 'login.html', {"message1":message1})
				else:
					message1="Username, Password or University is Incorrect"
#					message1="Invalid username or password."
					return render(request,'login.html', {"message1":message1} )
			else:		
				print(MyLoginForm.errors)
				message1="All fields are mandatory"
				return render(request,'login.html', {"message1":message1} )
			form = LoginForm()
			return redirect('/')
		else:
			return render(request, 'login.html')

#	return render(request, 'dashboard.html', {"username" : username})
def dashboard(request, username):
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).uploads!="-1":
			username1 = request.user.username
			if(username1==username):
				message1=""
				return render(request, 'dashboard.html', {"message1":message1, "username":username})
			else:
			#print(1)
				return redirect('/')
		else:
			return redirect('/')
	else:
		#print(2)
		return redirect('/')
def univdashboard(request, username):
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).uploads=="-1":
			sample=UserModel.objects.get(username=username)
			university=sample.university
			sample2=UserModel.objects.filter(university=university)
			details=""
			for user in sample2:
				if user.uploads!="-1":
		#if sample2.exists() and sample2.uploads!="-1":
				#details=""
				#for user in sample2:
					details=details+user.username+";"
		#username1 = request.user.username
		#if(username1==username):

			message1=""
			return render(request, 'univdashboard.html', {"message1":message1, "username":username, "details":details})
		else:
			#print(1)
			return redirect('/')
	else:
		#print(2)
		return redirect('/')
def signup(request):
	if request.user.is_authenticated:
		return redirect('dashboard', username=request.user.username)
	else:
		return render(request, 'signup.html')
def univsignup(request):
	if request.user.is_authenticated:
		return redirect('univdashboard', username=request.user.username)
	else:
		return render(request, 'univsignup.html')
def univcreatedaccount(request):
	if request.method == 'POST':
		form1 = NewUserForm(request.POST)
		form2 = SignForm(request.POST)
		if (form1.is_valid() and form2.is_valid()):
			#userd = UserModel.objects.create(username=form2.cleaned_data['username'], password=form2.cleaned_data['password1'], email=form2.cleaned_data['email'], university=form2.cleaned_data['university'], last_login=datetime.datetime.now())
			if not UserModel.objects.filter(university=form2.cleaned_data['university'], uploads="-1").exists() :
				userd=UserModel()
				userd.username = form2.cleaned_data['username']
				userd.university=form2.cleaned_data['university']
				userd.email=form2.cleaned_data['email']
				userd.last_login=datetime.datetime.now()
				userd.passcode=form2.cleaned_data['passcode']
				#if form2.cleaned_data['password1']==form2.cleaned_data['password2']:
				#userd.password=form2.cleaned_data['password1']
				userd.uploads="-1"
				userd.save()
				form1.save()
				message1="Account Created Succesfully"
				return render(request, 'login.html', {"message1":message1})
			else:
				message1="Account with same university already exists"
				return render(request, 'univsignup.html', {"message1":message1})
		else:
			message1=form1.errors
			message2=form2.errors
			print(message2)
			return render(request,'univsignup.html', {"message2":message2, "message1":message1} )
	form1 = UserCreationForm()
	message1="Invalid"
#	print ("hai")
	return render(request, "login.html", {"message1":message1})
def createdaccount(request):
	if request.method == 'POST':
		form1 = NewUserForm(request.POST)
		form2 = SignForm(request.POST)
		if (form1.is_valid() and form2.is_valid()):
			temp=test(request,form2.cleaned_data['university'], form2.cleaned_data['passcode'])
			if temp:
				#userd = UserModel.objects.create(username=form2.cleaned_data['username'], password=form2.cleaned_data['password1'], email=form2.cleaned_data['email'], university=form2.cleaned_data['university'], last_login=datetime.datetime.now())
				userd=UserModel()
				userd.username = form2.cleaned_data['username']
				userd.university=form2.cleaned_data['university']
				userd.email=form2.cleaned_data['email']
				userd.last_login=datetime.datetime.now()
				userd.passcode=form2.cleaned_data['passcode']
				#if form2.cleaned_data['password1']==form2.cleaned_data['password2']:
			 	#userd.password=form2.cleaned_data['password1']
			   	#userd.uploads=""
				userd.save()
				form1.save()
				message1="Account Created Succesfully"
				return render(request, 'login.html', {"message1":message1})
			else:
				message1="Invalid University or Passcode"
				return render(request, 'signup.html', {"message1":message1})
		else:
			message1=form1.errors
			message2=form2.errors
			print(message2)
			return render(request,'signup.html', {"message2":message2, "message1":message1} )
	form1 = UserCreationForm()
	message1="Invalid"
#	print ("hai")
	return render(request, "login.html", {"message1":message1})
def uploadfiles(request, username):
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
				sample=UserModel.objects.get(username=username)
				sample.uploads=sample.uploads+str(i)+";"
				sample.save()
				message1="Successfully Uploaded"
			else:
				message1="No file Uploaded"
#				print(MyProfileForm.errors)

				return render(request, 'dashboard.html', {"message1":message1, "username":username})
		else:
			MyProfileForm = Profileform()
		return render(request, 'dashboard.html', {"message1":message1, "username":username} )
	else:
		return redirect('/')
def logout1(request):
	username=None
	if request.user.is_authenticated:
		#username = request.user.username
		logout(request)
		message1="Logged Out Succesfully"
		return render(request, 'login.html', {"message1":message1})
		#return redirect('/', {"message1":message1})
	else:
		return redirect('/')
def changepassword(request, username):
	#username=None
	if request.user.is_authenticated:
		username1 = request.user.username
		if(username1==username):
			message1=""
			return render(request, 'changepassword.html', {"username":username})
		else:
			return redirect('/')
	else:
		return redirect('/')
def univchangepassword(request, username):
	#username=None
	if request.user.is_authenticated:
		username1 = request.user.username
		if(username1==username):
			message1=""
			return render(request, 'univchangepassword.html', {"username":username})
		else:
			return redirect('/')
	else:
		return redirect('/')
def savepassword(request, username):
	if request.user.is_authenticated:
		username=request.user.username
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				#sample=UserModel.objects.get(username=username)
				#sample.password=form.cleaned_data['']
				update_session_auth_hash(request, user)  # Important!
				message1="Your password has successfully updated!"
				return render(request, 'dashboard.html', {"username":username, "message1":message1})

			else:
				message1="Error Messages:"
				message2=form.errors
				return render(request, 'changepassword.html', {"message1":message1, "message2":message2, "username":username})
		else:
			form = PasswordChangeForm(request.user)
		message1=""
		return render(request, 'login.html', {"message1":message1, "username":username})
	else:
		return redirect('/')
def univsavepassword(request, username):
	if request.user.is_authenticated:
		username=request.user.username
		if request.method == 'POST':
			form = PasswordChangeForm(request.user, request.POST)
			if form.is_valid():
				user = form.save()
				#sample=UserModel.objects.get(username=username)
				#sample.password=form.cleaned_data['']
				update_session_auth_hash(request, user)  # Important!
				message1="Your password has successfully updated!"
				return redirect('univdashboard', username=request.user.username)

			else:
				message1="Error Messages:"
				message2=form.errors
				return render(request, 'univchangepassword.html', {"message1":message1, "message2":message2, "username":username})
		else:
			form = PasswordChangeForm(request.user)
		message1=""
		return render(request, 'login.html', {"message1":message1, "username":username})
	else:
		return redirect('/')

def temporary(request, temp):
	return redirect('/')
def yourfiles(request, username):
	if request.user.is_authenticated:
		sample=UserModel.objects.get(username=request.user.username)
		#context = Identity_unique.objects.filter(user=request.user)
		s=sample.uploads
		#s="1;2;3;4;5;6;7;8;9;0;10;11;12;13;14;15;16;17;18;19;20;"
		t=s.split(";")
#		print(t)
			#file[e]=(Profile.objects.filter(id=int(row)))
			#e=e+1
		context = {"username":username, 'file': Profile.objects.filter(id__in=t[:-1])}
#		print(context)
		return render(request, 'yourfiles.html', context);
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1})
def univfiles(request, univ, username):
	
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).uploads=="-1" and request.user.username==univ:
			sample=UserModel.objects.get(username=username)
			#if sample.university==univ:
			s=sample.uploads
			#s="1;2;3;4;5;6;7;8;9;0;10;11;12;13;14;15;16;17;18;19;20;"
			t=s.split(";")
#			print(t)
				#file[e]=(Profile.objects.filter(id=int(row)))
				#e=e+1
			context = {"username":univ, 'file': Profile.objects.filter(id__in=t[:-1])}
#			print(context)
			return render(request, 'indfiles.html', context);
		else:
			message1="Invalid"
			return redirect('/')
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
def test(request, university, passcode):
	org=university
	sample=UserModel.objects.filter(uploads="-1")
	if sample.exists():
		for user in sample:
			if (user.university==org):
				if(user.passcode==passcode):
					return True
				else:
					return False
	else:
		return False
	#else:
	#	if (org=="IIT Madras"):
	#		if (passcode==111111):
	#			return True
	#		else:
	#			return False
def forgotpassword2(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			username='pranayvarmas'
			associated_users = UserModel.objects.filter(email=data)
			#associated_users=authenticate(request, email=data, username=username)
			print(associated_users)
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password_reset_email.txt"
					global ran
					ran=random.randint(100000, 999999)
					#ran='ghrtue1234tub'
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					#"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					#'token': default_token_generator.make_token(user),
					'token':ran,
					'protocol': 'http',
					}
					print(ran)
					email = render_to_string(email_template_name, c)
					try:
					#print(user.email)
						send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=True)
						#print(1)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return render (request, 'forgotpassword2.html')
			else:
				return render(request, 'forgotpassword1.html', {"message1":"No user with this Email exists"})
	password_reset_form = PasswordResetForm()
	return redirect('/forgotpassword1/')
def forgotpassword1(request):
	return render(request, 'forgotpassword1.html')
def resetpassword(request):
	if request.method=="POST":
		reset_form=OtpForm(request.POST)
		if reset_form.is_valid():
			otp=reset_form.cleaned_data['otp']
			global ran
			if otp==ran:
				pass
#def orga(request):
#	if request.user.is_authenticated:
#		username=request.user.username
#		return render(request, 'organization.html', {"username":username})
#	else:
#		message1="Please login to enter Organization Passcode"
#		return render(request, 'login.html', {"message1":message1})
#def org(request):
#	if request.user.is_authenticated:
#		username=request.user.username
#		if request.method=="POST":
#			form=passcod(request.POST)
#			if form.is_valid():
#				passcode=form.cleaned_data["passcode"]
#				if(passcode==123456):
#					return render(request, 'dashboard.html', {"username":username})
#				else:
#					message1="Organization Passcode is incorrect"
#					return render(request, 'organization.html', {"username":username, "message1":message1})
#			else:
#				print(form.errors)
#				message1="Organization Passcode is Invalid"
#				return render(request, 'organization.html', {"username":username, "message1":message1})
#		else:
#			form=passcod()
#			message1="Organization Passcode is Invalid"
#			logoutin(request)
#			return render(request, 'login.html', {"message1":message1})
#	else:
#		message1="Please login to enter Organization Passcode"
#		return render(request, 'login.html', {"message1":message1})

