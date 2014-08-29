from django.shortcuts import get_object_or_404 , render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

#from django.template import RequestContext, loader

from polls.models import Question, Choice



# Standard view 
#def index(request):
#	return HttpResponse("Hello, World. You're at the polls index.")

# View with a collection of the latest 5 question available

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""Return the last five published questions. (not including those set to be published in the future.)"""
		# __LTE after field name means: LESS THAN or EQUAL
		# __GTE means GREATER THAN or EQUAL

		return Question.objects.filter(
		pub_date__lte=timezone.now(),
		).exclude( 
		    #Exlcude test if the question has choices through the foreign key and remove question with no answers. 
			choice__question__isnull=True
			).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
		Exclude any questions that aren't published yet
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	p = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = p.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question' : p, 
			'error_message' : "You didn't select a choice!",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		#Always return a ResponseRedirect after succesfully dealing
		# with POST. It prevents data being posted twice if a user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
