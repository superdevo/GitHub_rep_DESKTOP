from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from home.models import CustomUser, Countries, States, Cities
# Create your views here.
@login_required(login_url='/home/accounts/login/')
def load_geo(request):
	countries = Countries.objects.all().exclude(active=False).order_by('country_name')
	return render_to_response('browse/index.html', {'objs_c': countries},context_instance=RequestContext(request))

#Gets the AJAX request and return the states based on the country selected
def ajax_states(request):
	if request.is_ajax():
		country_id = request.GET['country_id']
		objs = States.objects.filter(country_id=country_id).order_by('state_name')
		return render_to_response('browse/geo_states.html',{ 'objs' : objs })

def ajax_cities(request):
	if request.is_ajax():
		state_id = request.GET['state_id']
		objs = Cities.objects.filter(state_id=state_id).order_by('city_name')
		return render_to_response('browse/geo_cities.html',{ 'objs' : objs })

def ajax_preview(request):
	if request.is_ajax():
		city_id = request.GET['city_id']
		city = Cities.objects.get(pk=city_id)
		state = States.objects.get(cities__id=city_id)
		country = Countries.objects.get(states__id=state.id)
		users = CustomUser.objects.filter(current_country=country.id, current_state=state.id, current_city=city.id)[:5]
		""" IMPORTANT
		I am using a lookup through related object (by foreign key).
		any user objects has a FOO_set that contains all post objects related to it.
		"""
		posts_count = 0
		for u in users:
			u.post_set.filter(is_active=True)
			posts_count += u.post_set.count()
		return render_to_response('browse/geo_preview.html',
			{'users' : users , 'posts_count' : posts_count, 'country':country.country_name, 'state':state.state_name, 'city' : city.city_name})