from django import forms
from django.forms import ModelForm
from home.models import Post

class PostForm(ModelForm):
	OPTIONS = ['Art', 'Engineering','IT', 'Medicine', 'Music']

	title = forms.CharField(max_length=100)
	content = forms.CharField(widget=forms.Textarea())
	keywords = forms.CharField(max_length=100)
	#forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
	#		choices=OPTIONS)
	class Meta:
		model = Post
		exclude = ('generating_user', 'country_ref', 'state_ref','city_ref','creation_date', 'is_active', 'is_offer',)
