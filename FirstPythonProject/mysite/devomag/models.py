from django.db import models

# Create your models here.

class Author(models.Model):
	auth_name = models.CharField(max_length=100)
	auth_nationality = models.CharField(max_length=100)
	auth_age = models.IntegerField()
	#THIS LETS YOU SEE PROPERLY THE OBJECT WHEN ADMINISTRATING. IT ALSO FIXES THE LIST POINTING TO OBJECTS IN FORM FROM MODELS
	def __unicode__(self):
       		return self.auth_name

class BlogEntry(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	pub_date = models.DateTimeField('date_published')
	author = models.ForeignKey(Author)
	
	def __unicode__(self):
       		return self.title
