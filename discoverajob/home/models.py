import datetime
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
"""
David: creating reference model for user override
"""

class Countries(models.Model):
	country_name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.country_name

class States(models.Model):
	country = models.ForeignKey(Countries)
	state_name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.state_name

class Cities(models.Model):
	state = models.ForeignKey(States)
	city_name = models.CharField(max_length=100)
	active = models.BooleanField(default=True)
	def __unicode__(self):
		return self.city_name



class CustomUser(models.Model):
	#  ****  Creating the list to display in the form for the user sign up extension ****
	
	objs_countries = Countries.objects.all()
	objs_states = States.objects.all()
	objs_cities = Cities.objects.all()

	COUNTRIES_CHOICES = [(x.id, x.country_name) for x in objs_countries]
	STATES_CHOICES = [(x.id, x.state_name) for x in objs_states]
	CITIES_CHOICES = [(x.id, x.city_name) for x in objs_cities]
	
	user = models.OneToOneField(User)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	birthday = models.DateField(null=True)
	age = models.IntegerField(null=True)

	current_country = models.IntegerField(choices=COUNTRIES_CHOICES, default=0)
	current_state = models.IntegerField(choices=STATES_CHOICES, default=0)
	current_city = models.IntegerField(choices=CITIES_CHOICES, default=0)

	profile_description = models.TextField()
	is_student = models.BooleanField(default=True)

	def __unicode__(self):
		return self.first_name

def create_customuser_user_callback(sender, instance,**kwargs):
	customuser, new = CustomUser.objects.get_or_create(user=instance)
post_save.connect(create_customuser_user_callback, User)


class Post(models.Model):
	generating_user = models.ForeignKey(CustomUser)
	country_ref = models.ForeignKey(Countries)
	state_ref = models.ForeignKey(States)#models.OneToOneField(states,to_field = 'id', db_index=True)
	city_ref = models.ForeignKey(Cities)#models.OneToOneField(cities,to_field = 'id', db_index=True)
	title = models.CharField(max_length=150)
	content = models.TextField()
	creation_date = models.DateTimeField(default=datetime.datetime.now(), db_index=True)
	is_active = models.BooleanField(default=False)
	is_offer = models.BooleanField()
	keywords = models.CharField(max_length=200)

	def get_absolute_url(self):
		return "/comm/post/%i/" % self.id

	def __unicode__(self):
		return  "%s - %s" % (self.title, self.generating_user.first_name)

class PostReview(models.Model):
    post = models.ForeignKey(Post)
    review_date = models.DateTimeField(blank = True, null=True)
    review_content = models.TextField(blank = True, null=True)
    review_stars = models.PositiveIntegerField(validators=[MaxValueValidator(5)],default=0)
    reviewing_user_id = models.ForeignKey(CustomUser)
