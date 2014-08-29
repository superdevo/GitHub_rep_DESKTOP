import datetime

from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import generic
from django.utils import timezone
from django.forms import ModelForm

from devomag.models import Author, BlogEntry

# Create your views here.

class IndexView(generic.ListView):
	template_name = 'devomag/index.html'
	#*** ATTENTION *** the name variable context_object_name is mandatory to talk with the INDEX.HTML!!
	context_object_name = 'blog_entries_list'

	def get_queryset(self):
		#First step: return all objects ...OK
		#Second step: return object not older than a week from now()
		time_span = timezone.now()
		time_span = time_span - datetime.timedelta(days=7) 
		return BlogEntry.objects.filter(pub_date__gte=time_span)

class DetailView(generic.DetailView):
	template_name = 'devomag/detail.html'
	model = BlogEntry
    
	def get_queryset(self):
		time_span = timezone.now()
		time_span = time_span - datetime.timedelta(days=7)
		"""
		try:
			obj = get_object_or_404(BlogEntry, self.kwargs['id'])
		except BlogEntry.DoesNotExist:
			raise Http404
		"""	
		obj = BlogEntry.objects.filter(pub_date__gte=time_span)
		if not obj:
			raise Http404
		else:	 
			return obj

class AuthDetailsView(generic.DetailView):
	template_name = 'devomag/auth_details.html'
	model = Author

	def get_queryset(self):

		return Author.objects.all()

class ArticleForm(ModelForm):
	class Meta:
		model = BlogEntry
		#i will use all fields ad mandatory

def NewArticle(request):
	if request.method == 'POST':
		"""
		After the form is submitted i clear the parameters and save it, redirecting to the thank you page.
		I will not do validation here becasue it is done client side with AJAX.
		"""	
		f =  ArticleForm(request.POST)
		if f.is_valid():
			f.save()
			return HttpResponseRedirect('/devomag/submit-new-article/thanks/')
		return render(request, 'devomag/newarticle.html', {'entry_form' : f })
	else:
		entry_form = ArticleForm()
		return render(request, 'devomag/newarticle.html', {'entry_form' : entry_form })

def thankyou(request):
	return render(request, 'devomag/thankyou.html')
