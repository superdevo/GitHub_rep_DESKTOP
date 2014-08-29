from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
     
class Drinker(models.Model):
	user = models.OneToOneField(User)
	birthday = models.DateField(blank=True, null=True)
	name = models.CharField(max_length=100)

	class Meta:
		permissions = (
			#permission identifier		Human readable permission-name
			('can_drink', 'Drinker can drink'),
			('can_eat', 'Drinker can eat'),
			('can_sing', 'Drinker can sing')
			)
	def __unicode__(self):
		return self.name

#create our user object to ttach to our drinker object
def create_drinker_user_callback(sender, instance, **kwargs):
	drinker, new = Drinker.objects.get_or_create(user=instance)
post_save.connect(create_drinker_user_callback, User)