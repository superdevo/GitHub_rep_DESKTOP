import datetime
import hashlib
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from home.models import Countries, States, Cities, Post, PostReview
from django.db.models import Q 
from comm.forms import PostForm

# Create your views here.
@login_required(login_url='/home/accounts/login/')
def comm_place(request,country,state,city):
	""" Remember to strip down the paramater and check whether it is correct or not. 
	and check whether the user is authenticated or not!!
	"""
	if request.user.is_authenticated():
		if request.user is not None:
			if request.user.customuser.is_student:
				is_offer=False
			else:
				is_offer=True
			try:	
				country = Countries.objects.get(country_name__iexact=country)
				state = States.objects.get(state_name__iexact=state)
				city = Cities.objects.get(city_name__iexact=city)
			except Countries.DoesNotExist:
				raise Http404
			except States.DoesNotExist:
				raise Http404
			except Cities.DoesNotExist:
				raise Http404
			
			"""
			qset = (
				Q(country_ref_id=country.id) |
				Q(state_ref_id=state.id) |
				Q(city_ref_id=city.id) |
				Q(is_active=True) |
				Q(is_offer=is_offer)
			)
			print qset
			"""	
			
			objs = Post.objects.filter(country_ref_id=country.id,
				state_ref_id=state.id,
				city_ref_id=city.id,
				is_active=True,
				is_offer=is_offer
				).exclude(generating_user=request.user.customuser.id).order_by('creation_date')

			return render_to_response('comm/index.html', {'objs' : objs},  context_instance=RequestContext(request))
	return HttpResponseRedirect('/home/')	

def create_post(request):
	if request.method == 'POST':
		p = PostForm(request.POST)
		if p.is_valid():
			"""
			After cleaning the form we create the post object based on user data and form info.
			After saving the form we redirect to a success page.
			"""
			
			generating_user = request.user.customuser
			country_ref = Countries.objects.get(pk=request.user.customuser.current_city)
			state_ref = States.objects.get(pk=request.user.customuser.current_state)
			city_ref = Cities.objects.get(pk=request.user.customuser.current_city)
			creation_date = datetime.datetime.now()

			if request.user.customuser.is_student:
				is_offer = False
			else:	
				is_offer = True

			post = Post(generating_user=generating_user, country_ref=country_ref, state_ref=state_ref, 
						city_ref=city_ref, creation_date=creation_date, is_active=True, is_offer=is_offer,
						title=p.cleaned_data['title'],content=p.cleaned_data['content'], keywords=p.cleaned_data['keywords'])
			post.save()

			#SAVE THE POST TO DB
			return HttpResponseRedirect('/comm/post/success/')
		return render_to_response('comm/new_post.html', { 'post' : post }, context_instance=RequestContext(request))
	post = PostForm()
	return render_to_response('comm/new_post.html', { 'post' : post }, context_instance=RequestContext(request))

def post_details(request, post_id):
	try:
		post = Post.objects.get(pk=post_id)
		rate_avg = 0
		if post.postreview_set.count() != 0:
			rate_tot=0
			for v in post.postreview_set.all():
				rate_tot += v.review_stars
			rate_avg = rate_tot/post.postreview_set.count()
	except Post.DoesNotExist:
		raise Http404	

	try:
		# Create a functon that checks whether the user has a cookie with a combination of:
		# user
		# poll_id
		post_choice_data_id = get_post_key_from_cookies(post, request.COOKIES)
		if post_choice_data_id is None:
			has_commented = False
		else:
			has_commented = True
	except KeyError:
		has_commented = False

	return render_to_response('comm/post_details.html', {'post' : post , 'has_commented': has_commented, 'rate':rate_avg}, context_instance=RequestContext(request))

def post_saved(request):
	# The state and city should be looked up based on the user instance
	state_name = 'Texas'
	city_name = 'Houston'

	return render_to_response('comm/post_success.html', {'state_name': state_name, 'city_name' : city_name}, context_instance=RequestContext(request))
def post_rate(request):
	if request.is_ajax():
		post_id = request.GET['post_id']
		rate = request.GET['rate']
		post = Post.objects.get(pk=post_id)

		post_rate = PostReview(post=post,reviewing_user_id=request.user.customuser)
		post_rate.review_date = datetime.datetime.now()
		post_rate.review_content = 'This is a first mockup of the rating mechanism'
		post_rate.review_stars = rate
		post_rate.save()
		#After the comment i set the cookie
		response = HttpResponse('<p>You have successfully rated this post.</p>')
		#PLEASE NOTE THAT:
		# we are not specifying a max age for the cookie, so this cookie will expire when the browser is closed.
		response.set_cookie(get_post_key(post),post_id)

		return response
		#render_to_response('comm/post_rate.html')
	raise Http404

def get_post_key(post):
	"""
	Method that creates a unique hash for each poll based on the URL
	"""
	return hashlib.sha224(post.get_absolute_url()).hexdigest()

def get_post_key_from_cookies(post, cookies):
	post_key = get_post_key(post)
	post_choice_data_id = cookies.get(post_key, None)
	return post_choice_data_id

"""
THis method can be added to the test on the rating portion of the view
in case permissions to vote are needed.

def user_can_vote(post_data_id):
	print post_data_id
	if post_data_id is not None:
		return False
	else:
		return True
"""