from django.shortcuts import get_object_or_404 , render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

#from django.template import RequestContext, loader

from polls.models import Question, Choice



# Standard view 
#def index(request):
#	return HttpResponse("Hello, World. You're at the polls index.")

# View with a collection of the latest 5 question available

def index(request):
        # VERSION 1 NOT OPTIMIZED (USES REMMED IMPORTS)-----------
	#latest_question_list = Question.objects.order_by('-pub_date')[:5]
	#template = loader.get_template('polls/index.html')
	#context = RequestContext(request, {
	#	'latest_question_list': latest_question_list,
	#})
	#return HttpResponse(template.render(context))
	#---------------------------------------------------------
	 
	#The context is a dictionary mapping template variable names to Python objects.
	# VERSION 2 OPTIMIZED
	latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
	context = {'latest_question_list' : latest_question_list}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	#VERSION 1 NOT OPTIMIZED    
        # try:
	# 	question = Question.objects.get(pk=question_id)
	# except Question.DoesNotExist:
	# 	raise Http404
	#------------------------------------------------------------
	# VERSION 2 OPTIMIZED: loose coupling catches and raises 404 automatically.

	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/detail.html", {'question' : question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)	
	return render(request, 'polls/results.html', {'question' : question})

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

