from django.shortcuts import render
#from django.shortcuts import render
from .forms import NewUserForm
from UI.forms import ProfileForm,SignForm, PasswordResetForm, PasscodeForm
from UI.models import Profile, UserModel, UniversityModel
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
#from new import myfunc
from shutil import copyfile
import pathlib
import csv
import zipfile
from os import listdir
from os.path import isfile, join
import shutil
import glob
#import mimetypes
import time
import sys ,os
import numpy as np
import tarfile
import re
import zipfile
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from os import listdir
from os.path import isfile, join
#import UI.cplusplus
#from UI import cplusplus
x=0
global ran

def login1(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
			username = request.user.username
			return redirect('dashboard', username=username)
		else:
			if UniversityModel.objects.filter(username=request.user.username).exists():
				username = request.user.username
				return redirect('univdashboard', username=username)
			else:
				if request.user.is_superuser:
					#logout(request)
					message1="Hey Admin, You are redirected to User Dashboard Page"
					return render(request, 'dashboard.html', {"message1":message1, "username":request.user.username})
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
					if UserModel.objects.filter(username=username).exists():
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
								return render(request, 'login.html', {"message1":message1, "links":links})
						else:
							message1="Invalid Passcode"
							return render(request, 'login.html', {"message1":message1, "links":links})
					else:
						if UniversityModel.objects.filter(username=username).exists():
							temp=test(request,university, passcode)
							if temp:
								sample=UniversityModel.objects.get(username=username)
								#print(sample.university)
								if sample.university==university:
									login(request, user)
									sample=UniversityModel.objects.get(username=request.user.username)
									sample.last_login=datetime.datetime.now()
									sample.save()
									#sec=request.user
									return redirect('univdashboard', username=request.user.username)
								else:
							#		logout(request)
									message1="University doesn't match"
									return render(request, 'login.html', {"message1":message1, "links":links})
							else:
								message1="Invalid Passcode"
								return render(request, 'login.html', {"message1":message1, "links":links})
						else:
							message1="No User Exists"
							return render(request, 'login.html', {"message1":message1, "links":links})
				else:
					message1="Username, Password or University is Incorrect"
#					message1="Invalid username or password."
					return render(request,'login.html', {"message1":message1, "links":links} )
			else:		
				#print(MyLoginForm.errors)
				message1="All fields are mandatory"
				return render(request,'login.html', {"message1":message1, "links":links} )
			form = LoginForm()
			return redirect('/')
		else:
			return render(request, 'login.html', {"links":links})

#	return render(request, 'dashboard.html', {"username" : username})
def dashboard(request, username):
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
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
		if UniversityModel.objects.filter(username=request.user.username).exists():
			sample=UniversityModel.objects.get(username=username)
			university=sample.university
			sample2=UserModel.objects.filter(university=university)
			details=""
			for user in sample2:
				#if user.uploads!="-1":
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
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).exists():
			return redirect('dashboard', username=request.user.username)
		else:
			if UniversityModel.objects.get(username=request.user.username).exists():
				return redirect('univdashboard', username=request.user.username)
			else:
				logout(request)
				message1:"We've encountered an unexpected error. Please login again"
				return render(request, 'login.html', {"message1":message1})

	else:
		return render(request, 'signup.html', {"links":links})
def univsignup(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UserModel.objects.get(username=request.user.username).exists():
			return redirect('dashboard', username=request.user.username)
		else:
			if UniversityModel.objects.get(username=request.user.username).exists():
				return redirect('univdashboard', username=request.user.username)
			else:
				logout(request)
				message1:"We've encountered an unexpected error. Please login again"
				return render(request, 'login.html', {"message1":message1})

	else:
		return render(request, 'univsignup.html', {"links":links})
def univcreatedaccount(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	#return render(request, 'login.html', {"message1":message1, "links":links})
	if request.method == 'POST':
		form1 = NewUserForm(request.POST)
		form2 = SignForm(request.POST)
		if (form1.is_valid()):
			if (form2.is_valid()):
				#print(1)
				#userd = UserModel.objects.create(username=form2.cleaned_data['username'], password=form2.cleaned_data['password1'], email=form2.cleaned_data['email'], university=form2.cleaned_data['university'], last_login=datetime.datetime.now())
				if not UniversityModel.objects.filter(university=form2.cleaned_data['university']).exists():
					if not UniversityModel.objects.filter(username=form2.cleaned_data['username']).exists():
						userd=UniversityModel()
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
						#return redirect('/')
						links=""
						links1=UniversityModel.objects.filter(uploads="-1")
						if links1.exists():
							for link in links1:
								links=links+link.university+";"
						return render(request, 'login.html', {"message1":message1, "links":links})
					else:
						message2="Account with same username already exists"
						return render(request, 'univsignup.html', {"message2":message2, "links":links})
				else:
					#print(1)
					message2="Account with same university already exists"
					return render(request, 'univsignup.html', {"message2":message2, "links":links})
			else:
				message2=form2.errors
				return render(request,'univsignup.html', {"message2":message2, "links":links} )
		else:
			#message1=form1.errors
			message2=form1.errors
			#print(message2)
			return render(request,'univsignup.html', {"message2":message2, "links":links} )
	form1 = UserCreationForm()
	#message1="Invalid"
#	print ("hai")
	#return render(request, "login.html", {"message1":message1, "links":links})
	return redirect('/')
def createdaccount(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.method == 'POST':
		form1 = NewUserForm(request.POST)
		form2 = SignForm(request.POST)
		if (form1.is_valid()):
			if(form2.is_valid()):
				#print(form2.cleaned_data['university'])
				temp=test(request,form2.cleaned_data['university'], form2.cleaned_data['passcode'])
				if temp:
					if not UserModel.objects.filter(username=form2.cleaned_data['username']).exists():
						#userd = UserModel.objects.create(username=form2.cleaned_data['username'], password=form2.cleaned_data['password1'], email=form2.cleaned_data['email'], university=form2.cleaned_data['university'], last_login=datetime.datetime.now())
						userd=UserModel()
						userd.username = form2.cleaned_data['username']
						userd.university=form2.cleaned_data['university']
						userd.email=form2.cleaned_data['email']
						userd.last_login=datetime.datetime.now()
						userd.passcode=form2.cleaned_data['passcode']
						#userd.set_password(form2.cleaned_data['password1'])
						#if form2.cleaned_data['password1']==form2.cleaned_data['password2']:
						#userd.password=form2.cleaned_data['password1']
						#userd.uploads=""
						userd.save()
						form1.save()
						message1="Account Created Succesfully"
						return render(request, 'login.html', {"message1":message1, "links":links})
					else:
						message2="Account with same username already exists"
						return render(request, 'signup.html', {"message2":message2, "links":links})
				else:
					#print(78)
					message2="Invalid University or Passcode"
					return render(request, 'signup.html', {"message2":message2, "links":links})
			else:
				message2=form2.errors
				return render(request,'signup.html', {"message2":message2, "links":links} )
		else:
			#message1=form1.errors
			message2=form1.errors
			#print(message2)
			return render(request,'signup.html', {"message2":message2, "links":links} )
	form1 = UserCreationForm()
	#message1="Invalid"
#	print ("hai")
	#return render(request, "login.html", {"message1":message1, "links":links})
	return redirect('/')
file1=pathlib.Path('')
name=None
def uploadfiles(request, username):
	saved = False
	username=None
	#print(1)
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
			#print(1)
			username = request.user.username
			if request.method == "POST":
	  #Get the posted form
				MyProfileForm = ProfileForm(request.POST, request.FILES)

				if MyProfileForm.is_valid():
					#print(1)
					profile = Profile()
					#profile.name = MyProfileForm.cleaned_data["name"]
					profile.picture = MyProfileForm.cleaned_data["picture"]
					profile.picture2=MyProfileForm.cleaned_data["picture"]
					if zipfile.is_zipfile(profile.picture):
						#print(1)
					#else:
						#print(2)
						profile.last_time=datetime.datetime.now()
						profile.save()
						saved = True
						i=Profile.objects.all().count()-1
						i=i+1
#						print(i)
						first=request.user
						sample=UserModel.objects.get(username=username)
						sample.uploads=sample.uploads+str(i)+";"
						sample.save()
						message1="Successfully Uploaded!  Validating......"
						t=sample.uploads.split(';')
						#print(t)
						#print(1)
						file=Profile.objects.get(id__in=t[-2:-1]).picture
						file2=Profile.objects.get(id__in=t[-2:-1]).picture2
						#print(file2)
						global name
						name=(str(file))
						name=name[0:-4]
						#name=name.split('_')[0:-1]
						#print(os.getcwd())
						current=os.getcwd()
						#copyfile(pathlib.Path(str(current)+'/uploads_cdn/'+str(file)),pathlib.Path(str(current)+'/input/'+str(file)))
						#os.rename("../input/"+str(file), "../input/inp.zip")
						file=pathlib.Path(str(current)+'/'+str(file2))
						#print(file)
						#print(2)
						language=MyProfileForm.cleaned_data['language']
						if(language=="C++"):
							cplusplus(file)
						else:
							if(language=="Python"):
								python(file)
							else:
								message1="Select language"
								return render(request, 'dashboard.html', {"message1":message1, "username":username})
						format1=MyProfileForm.cleaned_data['format1']
						if(format1=="Plot"):
							result1=str(current)+'/result/outplot.png'
						else:
							if(format1=="CSV"):
								result1=str(current)+'/result/outcsv.csv'
							else:
								message1="Select Download Format"
								return render(request, 'dashboard.html', {"message1":message1, "username":username})
						response=download_file(request, result1, request.user.username)
						for root, dirs, files in os.walk('./input/'):
							for f in files:
								os.unlink(os.path.join(root, f))
							for d in dirs:
								shutil.rmtree(os.path.join(root, d))
						#os.remove('./input/'+str(file2))
						return response
						#print(result)
						#return redirect('result', {"username":request.user.username, "filepath":result1})
					message1="Please upload a zip file"
					return render(request, 'dashboard.html', {"message1":message1, "username":username, })

				else:
					message1="No file Uploaded"
#					print(MyProfileForm.errors)

					return render(request, 'dashboard.html', {"message1":message1, "username":username})
			else:
				#MyProfileForm = Profileform()
				return render(request, 'dashboard.html', {"username":username} )
		else:
			return redirect('/')
	else:
		return redirect('/')
def download_file(request, path, username):
	#print("ai")
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	#print(file_path)
	if os.path.exists(file_path):
		#print("lp")
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			#print(response)
			return response
	raise Http404	
final=None
LIST=None
def cplusplus(file):
	#global t
	#t=1
	#time.sleep(60)
	global final
	final = c_evaluate(file)
	zip = zipfile.ZipFile(file)	
	# available files in the container
	global LIST
	LIST = zip.namelist()[:]
	del LIST[0]
	#LIST=None
	#print(final)
	#print(LIST)
	c_plots(final)
	final = final.astype('str')
	c_csv_write(final)
def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f
def c_unzip(fil):
	with zipfile.ZipFile(fil, 'r') as zip_ref:
		zip_ref.extractall('./input/')
	#os.remove('./input/inp.zip')
	#os.rename('../input/'+str(name), '../input/inp')
	#fil=pathlib.Path(str(os.getcwd())+'/input/')
	#print(fil)
	files = [join(fil.__str__()[0:len(fil.__str__())-4], f) for f in listdir_nohidden(fil.__str__()[0:len(fil.__str__())-4]) if isfile(join(fil.__str__()[0:len(fil.__str__())-4], f))]
	#print(files)
	return files

def c_merge(l):
	ans = ""
	for i in l:
		ans = ans + i
	return ans.replace('\n', ' ')

def c_eliminate_comments(dat):
	global final
	global LIST
	for i in range(len(dat)):
		ind = dat[i].find("/*")
		#print(ind)
		if (ind != -1) :
			#dat[i] = dat[i][0:ind] + "\n"
			j = i
			ind1 = dat[j].find("*/")
			while (ind1 == -1) :
				j = j + 1
				ind1 = dat[j].find("*/")
			#dat[i] = dat[i][0:ind] + "\n"
			for k in range(i+1, j):
				dat[k] = "\n"
			#dat[j] = dat[j][(ind1+1):]
			if (j == i) :
				dat[i] = dat[i][0:ind] + " " + dat[i][(ind1+2):]
			else :
				dat[i] = dat[i][0:ind] + "\n"
				dat[j] = dat[j][(ind1+2):]


	for i in range(len(dat)):
		ind = dat[i].find("//")
		#print(ind)
		if (ind != -1) :
			dat[i] = dat[i][0:ind] + "\n"
		return dat

def c_remove_functions(data):
	global final
	global LIST
	ind7 = data.find("int main")
	#print(ind7)	
	globa = data[0:ind7]
	globa = globa + "{"
	functions = {}
	ind = globa.find("{")
	#print(ind)
	#count = 0
	#print(len(globa))
	while (ind != -1):
		if (globa[(ind+1):].find("}")==-1):
			break
		if (globa[(ind+1):].find("{") < globa[(ind+1):].find("}")):
			ind1 = ind
			#print(ind1, "hi")
			while (globa[(ind1+1):].find("{") < globa[(ind1+1):].find("}")):
				#print
				count=ind1+1+globa[(ind1+1):].find("}")
				k=0
				while (ind1+1+globa[(ind1+1):].find("{") < count):
					#count=count-globa[(ind1+1):].find("{")
					ind1 = ind1+1 + globa[(ind1+1):].find("{")
					k=k+1
					#print k
				for i in range(k):
					ind1 = ind1+1 + globa[(ind1+1):].find("}")
				#print(ind1)
			ind1 = ind1+1 + globa[(ind1+1):].find("}")
			#print(ind1)
		else:
			ind1 = ind+1 + globa[(ind+1):].find("}")
			#print(ind1)
		#print(ind1)
		#print(ind, "ind")
		ind2 = globa[0:ind].rfind("(")
		#print(ind2, "ind2")
		#print(ind2)
		#count = count + 1
		#if (count == 10):
		#   break
		ind3 = 0
		ind4 = 0
		for c in range(ind2 - 1, 0, -1):
			if (globa[c] != " "):
				ind3 = c
				break
		for c in range(ind3, 0, -1):
			#print(c, "c")
			if (globa[c] == " "):
				ind4 = c + 1
				break
		#print(ind4, ind1+1)
		function = globa[ind4:(ind3+1)]
		functions[function] = globa[(ind+1):ind1]
		#print(function, globa[(ind+1):ind1])
		#print("break")
		globa = globa[0:ind4]+" "+globa[(ind1+1):]
		#print(len(globa), "jk")
		ind = globa.find("{")
		#print(ind)
	#print(data)
	data = globa + " " + data[ind7:]
	#print("hi")
	for w in list(functions.keys()):
		data = data.replace(w, functions[w])
	return data

def c_set_globvar(lengths):
	global final
	global LIST
	global x   # Needed to modify global copy of globvar
	x = len(lengths)


def c_find_signature(files):
	global final
	global LIST
	word_count_vector = []
	lengths = []
	for file in files:
		#print(file)
		with open(file, 'r') as f:
		#data = f.read().replace('\n', ' ')
		#print(data)
			#print(f)
			dat = f.readlines()
		#print(dat)
			dat = c_eliminate_comments(dat)
			#print(l)
		#print(dat)
			data = c_merge(dat)
		#print(data)
			data = c_remove_functions(data)
			data = re.sub(r'[^\w]', ' ', data)
		#lines.append(data)
			words = data.split(' ')
			words_unique = list(np.unique(np.array(words)))
			freq = {w : 0 for w in words_unique}
			for word in words:
				freq[word] = freq[word] + 1
			freq.pop('')
			word_count_vector.append(list(freq.values()))
			lengths.append(len(freq))
			c_set_globvar(lengths)
	return [word_count_vector, lengths]

def c_sort_pad(lengths, word_count_vector):
	global final
	global LIST
	final_length = max(lengths)
	for w in word_count_vector:
		if (len(w) == final_length):
			w.sort()
			continue
		else:
			num = final_length - len(w)
			for i in range(num):
				w.append(0)
			w.sort()
	return [word_count_vector, final_length]

def c_normalize(word_count_vector, final_length):
	global final
	global LIST
	final_word_count = [[] for j in range(final_length)]

	for w in word_count_vector:
		for i in range(final_length):
			final_word_count[i].append(w[i])

	means = [np.mean(np.array(final_word_count[j])) for j in range(final_length)]
	stds = [np.std(np.array(final_word_count[j])) for j in range(final_length)]
#print(means)
#print(stds)
	for w in word_count_vector:
		for i in range(final_length):
			if (stds[i] == 0):
				continue
			w[i] = (w[i] - means[i])/stds[i]
	return word_count_vector

def c_similar(word_count_vector):
	global final
	global LIST
	#print(final)
	an = [0 for i in range(len(word_count_vector))]
	ad = [an for i in range(len(word_count_vector))]
	final = np.array(ad, dtype=float)
	for i in range(len(word_count_vector)):
		for j in range(len(word_count_vector)):
			#if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
			#	val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
			#if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
			#	val=1.0;
			val = 1-np.linalg.norm(np.array(word_count_vector[i]) - np.array(word_count_vector[j]))/max(np.linalg.norm(np.array(word_count_vector[i])), np.linalg.norm(np.array(word_count_vector[j])))
			final[i][j] = val
	#print(final)
	return final

def c_evaluate(zip):
	global final
	global LIST
	files = c_unzip(zip)
	#print(files)
	[word_count_vector, lengths] = c_find_signature(files)
	[word_count_vector, final_length] = c_sort_pad(lengths, word_count_vector)
	#word_count_vector = c_normalize(word_count_vector, final_length)
	#print(word_count_vector)
	final = c_similar(word_count_vector)
	#print(final)
	return final
def c_csv_write(final):
	#global final
	global LIST
	current=str(os.getcwd())
	total=current+'/result/outcsv.csv'
	file = open(pathlib.Path(total), 'wb')
	file1 = open(pathlib.Path(total), 'a+', newline ='')
	# writing the data into the file
	l = [i for i in range(0,x+1)]
	for i in range(0, len(l)):
		if(i==0):
			l[i] = 'files'
		if(i!=0): 
			l[i] = 'w.r.t '+str(LIST[i-1])
	arr = [i for i in range(1,x+1)]
	for i in range(0,len(arr)):
		arr[i] = str(LIST[i])
	arr = np.array(arr)
	result = np.hstack((final, np.atleast_2d(arr).T))
	for i in range(x):
		result[:, [x-i, x-i-1]] = result[:, [x-i-1, x-i]] 
# writing the data into the file
	i=0
	with file1:
		if(i==0):
			write = csv.writer(file1) 
			write.writerow(l) 
			i=1
		if(i!=0):        
			write = csv.writer(file1) 
			write.writerows(result)
def c_plots(final):
	#global final
	global LIST
	#print(final)
	fig = plt.figure()
	ax = sns.heatmap(final, linewidth=0.5,cmap="hot")
	ax.set_xticks(np.arange(len(LIST)))
	ax.set_yticks(np.arange(len(LIST)))
# ... and label them with the respective list entries
	ax.set_xticklabels(LIST)
	ax.set_yticklabels(LIST)

# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
		 rotation_mode="anchor")
	plt.setp(ax.get_yticklabels(), rotation=360, ha="right",
		rotation_mode="anchor")
	current=str(os.getcwd())
	total=current+'/result/outplot.png'
	fig.savefig(pathlib.Path(total), bbox_inches='tight', dpi=150)

# Loop over data dimensions and create text annotations.
	ax.set_title("RESULT")
	#plt.show()
def python(file):
	global final
	final=None
	final = p_evaluate(file)
	zip = zipfile.ZipFile(file)
	# available files in the container
	global LIST
	LIST=None
	LIST = zip.namelist()[:]
	del LIST[0]
	p_plots(final)
	final = final.astype('str')
	p_csv_write(final)
x=0
def p_unzip(fil):
	with zipfile.ZipFile(fil, 'r') as zip_ref:
		zip_ref.extractall('./input/')
	files = [join(fil.__str__()[0:len(fil.__str__())-4], f) for f in listdir(fil.__str__()[0:len(fil.__str__())-4]) if isfile(join(fil.__str__()[0:len(fil.__str__())-4], f))]
	return files

#lines = []
def p_merge(l):
	ans = ""
	for i in l:
		ans = ans + i
	return ans.replace('\n', ' ')

def p_edit_functions(dat):
	global final
	global LIST
	functions = {}
	for i in range(len(dat)-1):
		if (dat[i].find("def") != -1):
			ind1 = dat[i].find("def") + 3
			for k in range(ind1+1, len(dat[i])):
				if (dat[i][k] != " "):
					ind1 = k
					break
			ind2 = 0
			for k in range(ind1, len(dat[i])):
				if (dat[i][k] == " " or dat[i][k] == "("):
					ind2 = k - 1
					break
			function = dat[i][ind1:(ind2+1)]
			ind3 = dat[i].find(":")
			definition = ""
			for k in range(ind3+1, len(dat[i])-2):
				if (dat[i][k] != " "):
					ind4 = i
					definition = dat[i][ind4:]
					break
			if (definition != ""):
				functions[function] = definition
				dat[i]= dat[i][0:ind1] + "\n"
				continue
			else:
				for k in range(len(dat[i+1])):
					if (dat[i+1][k] != " "):
						ind4 = k
						break

				ind6 = 0
				for k in range(i+1, len(dat)):
					for l in range(len(dat[k])):
						if (dat[k][l] != " "):
							ind5 = l
							break
					if (ind4 > ind5):
						ind6 = k - 1
						break
				definition = p_merge(dat[i:(ind6+1)])
				#print(function, "hi")
				functions[function] = definition
				#print(function, definition)
				dat[i]= dat[i][0:ind1] + "\n"
				for g in range(i+1, ind6+1):
					dat[g] = "\n"
	return [dat, functions]

def p_eliminate_comments(dat):
	global final
	global LIST
	for i in range(len(dat)):
		ind = dat[i].find("#")
		#print(ind)
		if (ind != -1) :
			dat[i] = dat[i][0:ind] + "\n"
	return dat
def p_set_globvar(lengths):
	global final
	global LIST
	global x   # Needed to modify global copy of globvar
	x = len(lengths)
def p_find_signature(files):
	global final
	global LIST
	word_count_vector = []
	lengths = []
	for file in files:
		with open(file, 'r') as f:
		#data = f.read().replace('\n', ' ')
		#print(data)
			dat = f.readlines()
		#print(dat)
			dat = p_eliminate_comments(dat)
			#print(l)
		#print(dat)
			[dat, functions] = p_edit_functions(dat)
			data = p_merge(dat)
			for w in list(functions.keys()):
				data.replace(w, functions[w])
			#print(w)
			#print(data)
			#print(functions)
		#print(data)
			data = re.sub(r'[^\w]', ' ', data)
		#lines.append(data)
			words = data.split(' ')
			words_unique = list(np.unique(np.array(words)))
			freq = {w : 0 for w in words_unique}
			for word in words:
				freq[word] = freq[word] + 1
			freq.pop('')
			word_count_vector.append(list(freq.values()))
			lengths.append(len(freq))
			p_set_globvar(lengths)
	return [word_count_vector, lengths]

#print(word_count_vector)
#print(lengths)
def p_sort_pad(lengths, word_count_vector):
	global final
	global LIST
	final_length = max(lengths)
	for w in word_count_vector:
		if (len(w) == final_length):
			w.sort()
			continue
		else:
			num = final_length - len(w)
			for i in range(num):
				w.append(0)
			w.sort()
	return [word_count_vector, final_length]

#print(word_count_vector)
def p_normalize(word_count_vector, final_length):
	global final
	global LIST
	final_word_count = [[] for j in range(final_length)]

	for w in word_count_vector:
		for i in range(final_length):
			final_word_count[i].append(w[i])

	means = [np.mean(np.array(final_word_count[j])) for j in range(final_length)]
	stds = [np.std(np.array(final_word_count[j])) for j in range(final_length)]
#print(means)
#print(stds)
	for w in word_count_vector:
		for i in range(final_length):
			if (stds[i] == 0):
				continue
			w[i] = (w[i] - means[i])/stds[i]
	return word_count_vector
#print(word_count_vector)
def p_similar(word_count_vector):
	global final
	global LIST
	an = [0 for i in range(len(word_count_vector))]
	ad = [an for i in range(len(word_count_vector))]
	final = np.array(ad, dtype=float)
	for i in range(len(word_count_vector)):
		for j in range(len(word_count_vector)):
			#if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))!=0):
			#	val = np.dot(np.array(word_count_vector[i]), np.array(word_count_vector[j])) / (np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))
			#if((np.linalg.norm(np.array(word_count_vector[i]))*np.linalg.norm(np.array(word_count_vector[j])))==0):
			#	val=1.0;
			val = 1-np.linalg.norm(np.array(word_count_vector[i]) - np.array(word_count_vector[j]))/max(np.linalg.norm(np.array(word_count_vector[i])), np.linalg.norm(np.array(word_count_vector[j])))
			final[i][j] = val
	return final
def p_evaluate(zip):
	global final
	global LIST
	files = p_unzip(zip)
	[word_count_vector, lengths] = p_find_signature(files)
	[word_count_vector, final_length] = p_sort_pad(lengths, word_count_vector)
	#word_count_vector = p_normalize(word_count_vector, final_length)
	final = p_similar(word_count_vector)
	#print(final)
	return final
def p_csv_write(final):
	#global final
	global LIST
	current=str(os.getcwd())
	total=current+'/result/outcsv.csv'
	file = open(pathlib.Path(total), 'wb')
	file1 = open(pathlib.Path(total), 'a+', newline ='')
# writing the data into the file
	l = [i for i in range(0,x+1)]
	for i in range(0, len(l)):
		if(i==0):
			l[i] = 'files'
		if(i!=0): 
			l[i] = 'w.r.t '+str(LIST[i-1])
	arr = [i for i in range(1,x+1)]
	for i in range(0,len(arr)):
		arr[i] = str(LIST[i])
	arr = np.array(arr)
	result = np.hstack((final, np.atleast_2d(arr).T))
	for i in range(x):
		result[:, [x-i, x-i-1]] = result[:, [x-i-1, x-i]] 
# writing the data into the file
	i=0
	with file1:
		if(i==0):
			write = csv.writer(file1) 
			write.writerow(l) 
			i=1
		if(i!=0):        
			write = csv.writer(file1) 
			write.writerows(result)
def p_plots(final):
	#global final
	global LIST
	fig = plt.figure()
	ax = sns.heatmap(final, linewidth=0.5,cmap="hot")
	ax.set_xticks(np.arange(len(LIST)))
	ax.set_yticks(np.arange(len(LIST)))
# ... and label them with the respective list entries
	ax.set_xticklabels(LIST)
	ax.set_yticklabels(LIST)
	ax.set_title("RESULT")
# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=90, ha="right",
		 rotation_mode="anchor")
	plt.setp(ax.get_yticklabels(), rotation=360, ha="right",
		rotation_mode="anchor")
	current=str(os.getcwd())
	total=current+'/result/outplot.png'
	fig.savefig(pathlib.Path(total), bbox_inches='tight', dpi=150)
	#plt.show()
def logout1(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	username=None
	if request.user.is_authenticated:
		#username = request.user.username
		logout(request)
		message1="Logged Out Succesfully"
		return render(request, 'login.html', {"message1":message1, "links":links})
		#return redirect('/', {"message1":message1})
	else:
		return redirect('/')
def changepassword(request, username):
	#username=None
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
			username1 = request.user.username
			if(username1==username):
				message1=""
				return render(request, 'changepassword.html', {"username":username})
			else:
				return redirect('/')
		else:
			return redirect('/')
	return redirect('/')
def univchangepassword(request, username):
	#username=None
	if request.user.is_authenticated:
		if UniversityModel.objects.filter(username=request.user.username).exists():
			username1 = request.user.username
			if(username1==username):
				message1=""
				return render(request, 'univchangepassword.html', {"username":username})
			else:
				return redirect('/')
		else:
			return redirect('/')
	return redirect('/')
def savepassword(request, username):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
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
				return render(request, 'changepassword.html', {"username":username})
		else:
			return redirect('/')
	else:
		return redirect('/')
def univsavepassword(request, username):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UniversityModel.objects.filter(username=request.user.username).exists():
			username=request.user.username
			if request.method == 'POST':
				form = PasswordChangeForm(request.user, request.POST)
				if form.is_valid():
					user = form.save()
					#sample=UserModel.objects.get(username=username)
					#sample.password=form.cleaned_data['']
					update_session_auth_hash(request, user)  # Important!
					message1="Your password has successfully updated!"
					return render(request, 'univdashboard.html', {"username":username, "message1":message1})

				else:
					message1="Error Messages:"
					message2=form.errors
					return render(request, 'univchangepassword.html', {"message1":message1, "message2":message2, "username":username})
			else:
				form = PasswordChangeForm(request.user)
				message1=""
				return render(request, 'univchangepassword.html', {"username":username})
		else:
			return redirect('/')
	else:
		return redirect('/')
def temporary(request, temp):
	return redirect('/')
def yourfiles(request, username):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
			sample=UserModel.objects.get(username=request.user.username)
			#context = Identity_unique.objects.filter(user=request.user)
			s=sample.uploads
			#s="1;2;3;4;5;6;7;8;9;0;10;11;12;13;14;15;16;17;18;19;20;"
			t=s.split(";")
#			print(t)
				#file[e]=(Profile.objects.filter(id=int(row)))
				#e=e+1
			context = {"username":request.user.username, 'file': Profile.objects.filter(id__in=t[:-1])}
#			print(context)
			return render(request, 'yourfiles.html', context);
		else:
			return redirect('/')
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1, "links":links})
def univfiles(request, univ, username):
	
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=username).exists():
			sample=UserModel.objects.get(username=username)
			if UniversityModel.objects.filter(username=univ).exists():
				sample2=UniversityModel.objects.get(username=univ)
				if sample2.university==sample.university:
					s=sample.uploads
					#s="1;2;3;4;5;6;7;8;9;0;10;11;12;13;14;15;16;17;18;19;20;"
					t=s.split(";")
#					print(t)
						#file[e]=(Profile.objects.filter(id=int(row)))
						#e=e+1
					context = {"username":univ, 'file': Profile.objects.filter(id__in=t[:-1])}
#					print(context)
					return render(request, 'indfiles.html', context);
				else:
					message1="You don't have access to this user files"
					return render(request, 'univdashboard.html', {"message1":message1})
			else:
				return redirect('/')
		else:
			#message1="Invalid"
			return redirect('/')
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1})
def download(request, path):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UserModel.objects.filter(username=request.user.username).exists():
			file_path = os.path.join(settings.MEDIA_ROOT, path)
			if os.path.exists(file_path):
				with open(file_path, 'rb') as fh:
					response = HttpResponse(fh.read(), content_type="application/py")
					response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
					return response
			raise Http404
		else:
			return redirect('/')
	else:
		message1="Please login to download the files"
		return render(request,'login.html', {"message1":message1, "links":links})
def test(request, university, passcode):
	org=university
	#print(org)
	#print(passcode)
	sample=UniversityModel.objects.filter(university=org, uploads="-1")
	#print(sample)
	if sample.exists():
		for user in sample:
			if (user.university==org):
				if(user.passcode==passcode):
					return True
				else:
					#print(12)
					return False
	else:
		#print(90)
		return False
	#else:
	#	if (org=="IIT Madras"):
	#		if (passcode==111111):
	#			return True
	#		else:
	#			return False
def forgotpassword2(request):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			username='pranayvarmas'
			associated_users = UserModel.objects.filter(email=data)
			#associated_users=authenticate(request, email=data, username=username)
			#print(associated_users)
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
					#print(ran)
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
	return redirect('/')
	if request.method=="POST":
		reset_form=OtpForm(request.POST)
		if reset_form.is_valid():
			otp=reset_form.cleaned_data['otp']
			global ran
			if otp==ran:
				pass
def changepasscode(request, username):
	if request.user.is_authenticated:
		if UniversityModel.objects.filter(username=request.user.username).exists():
			username1 = request.user.username
			if(username1==username):
				message1=""
				return render(request, 'changepasscode.html', {"username":username1})
			else:
				return redirect('/')
		else:
			return redirect('/')
	return redirect('/')
def savepasscode(request, username):
	links=""
	links1=UniversityModel.objects.filter(uploads="-1")
	if links1.exists():
		for link in links1:
			links=links+link.university+";"
	if request.user.is_authenticated:
		if UniversityModel.objects.filter(username=request.user.username).exists():
			sample=UniversityModel.objects.get(username=request.user.username)
			username=request.user.username
			if request.method == 'POST':
				form = PasscodeForm(request.POST)
				if form.is_valid():
					passcode0=form.cleaned_data['passcode0']
					passcode1=form.cleaned_data['passcode1']
					passcode2=form.cleaned_data['passcode2']
					if(sample.passcode==passcode0):
						if(passcode1==passcode2):
							sample.passcode=passcode1
							sample.save()
							return redirect('univdashboard',username=request.user.username)
						else:
							message1="Error Messages"
							message2="New passcodes don't match"
							return render(request, 'changepasscode.html', {"message1":message1, "message2":message2, "username":request.user.username})
					else:
						message1="Error Messages"
						message2="Old Passcode doesn't match"
						return render(request, 'changepasscode.html', {"message1":message1, "message2":message2, "username":request.user.username})
				else:
					message1="Error Messages:"
					message2=form.errors
					return render(request, 'changepasscode.html', {"message1":message1, "message2":message2, "username":username})
			else:
				#form = PasswordChangeForm(request.user)
				#message1=""
				return render(request, 'changepasscode.html', {"username":username})
		else:
			return redirect('/')
	else:
		return redirect('/')
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

