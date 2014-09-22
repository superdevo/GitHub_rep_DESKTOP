from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
#---------- IMPORT for queries ----------
from django.db.models import Q 
from books.models import Book, PublisherForm, Author
from forms import ContactForm
from django.core.mail import send_mail
from django.views import generic
from django.utils import timezone
#----------------------------------------

# Create your views here.

"""
request.GET.get('q', ''):
	we access the GET with a Python method get() that returns null if no query has been specified! (SAFETY REASONS)
Q:
	is an object used to build complex queries

icontains:
	creates a case-sensitive LIKE statement in the query object.
"""

class IndexView(generic.ListView):
	template_name = 'index.html'
	context_object_name = 'list_of_books'
	paginate_by=5

	def get_queryset(self):
		return Book.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date') #[:5]


def search(request):
	query = request.GET.get('q', '')
	if query:
		qset = (
			Q(title__icontains=query) |
			Q(authors__first_name__icontains=query) |
			Q(authors__last_name__icontains=query)
		)
		results = Book.objects.filter(qset).distinct()
	else:
		results = []
	return render_to_response("search.html", {
		'results' : results,
		'query' : query
		})

def contact(request):
	if request.method == 'POST':
		f = ContactForm(request.POST)
		if f.is_valid():
			topic = f.cleaned_data['topic']
			message = f.cleaned_data['message']
			sender = f.cleaned_data.get('sender','noreply@books.com')
			"""
			send_mail(
				'Feedback from your site, topic: %s' % topic,
				message, sender,
				['david.torreggiani@gmail.com']
			)
			"""
			return HttpResponseRedirect('thanks/')
		else:
			return render(request, 'contact.html', {'contact_form':f})
	else:	
		f = ContactForm()
	return render(request, 'contact.html', {'contact_form':f})

def add_publisher(request):
	if request.method == 'POST':
		f = PublisherForm(request.POST)
		if f.is_valid():
			f.save()
			return HttpResponseRedirect('thanks/')
		else:
			return render(request, 'add_publisher.html', {'form' : f})
	else:
		f = PublisherForm()
		return render(request, 'add_publisher.html',{'form' : f})

# 		VEDI URL PER REDIRECT A TEMPLATE WITHOUT A VIEW!!!!!!!!
#def thankyou(request):
#	return render(request, 'thankyou.html')
def show_authors(request):
	authors_list = Author.objects.all()
	return render_to_response('authors.html', {'authors' : authors_list })

def load_image(request):
	image_data = open("/Users/dtorreg/Desktop/djangocourse/mysite/tmp/309637_185255791560170_1929264381_n.jpg", "rb").read()
	return HttpResponse(image_data, mimetype="image/jpeg")
