from django import forms
from books.models import Publisher


TOPIC_CHOICES = (
	('general','General enquiry'),
	('bug','Bug report'),
	('suggestion','Suggestion'),
)

class ContactForm(forms.Form):
	topic = forms.ChoiceField(choices=TOPIC_CHOICES)
	message = forms.CharField(widget=forms.Textarea(),initial="Replace with your feedback")
	sender = forms.EmailField(required=False)

	#This is an example of how to create a custom validation rule!
	def clean_message(self):
		message = self.cleaned_data.get('message', '')
		num_words = len(message.split(' '))
		if num_words < 4:
			raise forms.ValidationError("Not enough words!")
		return message
	