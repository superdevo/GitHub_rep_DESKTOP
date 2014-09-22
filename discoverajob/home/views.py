from django.shortcuts import render, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext, Context
from home.forms import SignUpForm
from home.models import CustomUser, Countries, Cities, States
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
	if request.user.is_authenticated():
		if request.user is not None:
			user_country = request.user.customuser.get_current_country_display()#Countries.objects.get(pk=request.user.customuser.current_country)
			user_state = request.user.customuser.get_current_state_display()#States.objects.get(pk=request.user.customuser.current_state)
			user_city = request.user.customuser.get_current_city_display()#Cities.objects.get(pk=request.user.customuser.current_city)
			return HttpResponseRedirect(reverse('comm_place', args=(user_country, user_state, user_city,)))
	#This test cookie will be verified when logging in.
	request.session.set_test_cookie()
	return render_to_response('home/index.html', context_instance=RequestContext(request))

def register_user(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/home/accounts/profile/')
	if request.method == 'POST':
		sign_up_form = SignUpForm(request.POST)
		if sign_up_form.is_valid():
			user = User.objects.create_user(username= sign_up_form.cleaned_data['username'], email= sign_up_form.cleaned_data['email'], password= sign_up_form.cleaned_data['password'], first_name = sign_up_form.cleaned_data['first_name'])
			user.save()

			custom_user = CustomUser.objects.get(user=user)
			custom_user.username = sign_up_form.cleaned_data['username']
			custom_user.first_name = sign_up_form.cleaned_data['first_name']
			custom_user.last_name = sign_up_form.cleaned_data['last_name']
			custom_user.birthday = sign_up_form.cleaned_data['birthday']
			custom_user.age = int(sign_up_form.cleaned_data['age'])
			custom_user.current_country = int(sign_up_form.cleaned_data['current_country'])
			custom_user.current_state = int(sign_up_form.cleaned_data['current_state'])
			custom_user.current_city = int(sign_up_form.cleaned_data['current_city'])
			custom_user.profile_description = sign_up_form.cleaned_data['profile_description']
			if sign_up_form.cleaned_data['is_student'] == "on":
				custom_user.is_student = True
			else:
				custom_user.is_student = False
			custom_user.save()

			user = authenticate(username=request.POST['username'], password=request.POST['password'])

			if user is not None:
				if user.is_active:
					login(request, user)
					#USE REVERSE AND LOAD THE ID!
					return HttpResponseRedirect('/home/accounts/profile/' + str(custom_user.id))
			else:
				return HttpResponseRedirect('/home/accounts/activate/') 
		else:
			return render_to_response('home/register.html',{'sign_up_form' : sign_up_form }, context_instance=RequestContext(request))	
	else:
		sign_up_form = SignUpForm()			
	return render_to_response('home/register.html',{'sign_up_form' : sign_up_form }, context_instance=RequestContext(request))

def login_user(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				"""
				After login in the request, i create the session
				"""
				request.session['customuser_id'] = user.customuser.id

				""" IMPORTANT
				instead of hitting the database to retrieve related country state city, i use:

				get_FOO_display()
				because the fields i need are binded to a list. The method will do the reverse look-up for me.
				"""

				user_country = user.customuser.get_current_country_display()#Countries.objects.get(pk=request.user.customuser.current_country)
				user_state = user.customuser.get_current_state_display()#States.objects.get(pk=request.user.customuser.current_state)
				user_city = user.customuser.get_current_city_display()#Cities.objects.get(pk=request.user.customuser.current_city)
				return HttpResponseRedirect(reverse('comm_place', args=(user_country, user_state, user_city,)))
			return HttpResponseRedirect('/home/accounts/activate/')
			
		else:
			return render_to_response('home/login_error.html',  context_instance=RequestContext(request)) 

	#Setting the test cookie

	request.session.set_test_cookie()
	return render_to_response('home/index.html', context_instance=RequestContext(request))

def logout_user(request):
	try:
		del request.session['customuser_id']
		logout(request)
		return HttpResponseRedirect('/home/')
	except KeyError:
		return HttpResponseRedirect('/home/')

@login_required(login_url='/home/accounts/login/')
def load_profile(request, profile_id):
    
	if profile_id == request.user.customuser.id:
		related_city = request.user.customuser.get_current_country_display()#Cities.objects.get(pk=request.user.customuser.current_city)
		related_state = request.user.customuser.get_current_state_display()#States.objects.get(pk=request.user.customuser.current_state)
		profile = request.user.customuser
	else:
		try:
			profile = CustomUser.objects.get(pk=profile_id)
		except CustomUser.DoesNotExist:
			raise Http404

		related_city = profile.get_current_city_display()#Cities.objects.get(pk=profile.current_city)
		related_state = profile.get_current_state_display()#States.objects.get(pk=profile.current_state)

	return render_to_response('home/profile.html', {'current_city' : related_city, 'current_state' : related_state, 'profile' : profile},  context_instance=RequestContext(request))
	
