from django.db import models
from django.contrib import admin
from django.forms import ModelForm

# Create your models here.
class Publisher(models.Model):
	name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60)
	state_province = models.CharField(max_length=30)
	country = models.CharField(max_length=50)
	website = models.URLField()

	#this tells Django to return only the name as part of the query.
	#It lets you filter by other fields in model regardless.
	def __str__(self):
		return self.name

	#This tells Django to order the query per name (by default)
	class Meta:
		ordering = ["name"]

	#Activate the Admin interface
	class Admin:
		pass

class PublisherForm(ModelForm):
	class Meta:
		model = Publisher

class Author(models.Model):
	salutation = models.CharField(max_length=10)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=40)
	email = models.EmailField()
	headshot = models.ImageField(upload_to='tmp')

	def __str__(self):
		return '%s %s' % (self.first_name, self.last_name)

	#Activate the Admin interface
	class Admin:
		pass

class Book(models.Model):
	title = models.CharField(max_length=100)
	authors = models.ManyToManyField(Author)
	publisher = models.ForeignKey(Publisher)
	publication_date = models.DateField()
	num_pages = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return self.title	

	#Activate the Admin interface
	class BookAdmin(admin.ModelAdmin):
		fields = ('title', 'publisher', 'publication_date')
		list_filter = ('publisher','publication_date')
		ordering = ('-publication_date',)
		search_fields = ('title',)
