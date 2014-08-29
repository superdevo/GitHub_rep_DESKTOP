from django.db import models

# Create your models here.

class NewsItem(models.Model):
	title = models.CharField(max_length=100)
	description = models.CharField(max_length=200)
	link = models.CharField(max_length=100)
	pub_date = models.DateField()

	def __unicode__(self):
		return self.title