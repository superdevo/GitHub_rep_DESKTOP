from django.forms import ModelForm
from home.models import CustomUser
from django.contrib.auth.models import User
from django import forms

class SignUpForm(ModelForm):
	username = forms.CharField(label=u'User Name')
	email = forms.EmailField(label=u'Email Address')
	password = forms.CharField(label=u'Password', widget=forms.PasswordInput(render_value=False))
	password1 = forms.CharField(label=u'Verify Password', widget=forms.PasswordInput(render_value=False))

	class Meta:
		model = CustomUser
		exclude = ('user',)


	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError("That username is taken.")

	"""
	If you do the clean it will add all the form value to the list clean_data, whether if you call specific clean (like clean_password)
	it will run for the password field and, since the form did not yet eveluated password1 the match would not work!
	"""
	def clean(self):
		password = self.cleaned_data['password']
		password1 = self.cleaned_data['password1']

		if password != password1:
			raise forms.ValidationError("Passwords don't match, try again")
		return self.cleaned_data
