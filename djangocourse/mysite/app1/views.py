#from django.shortcuts import render, render_to_response
from django.template import Template, Context
#from django.template.loader import get_template
#from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
# Create your views here.

""" Method with HttpResponse
def current_time(request):
	now = datetime.datetime.now()
	t= get_template('mytemplate.html')
	
	#t = Template("<html><body>It is now {{ current_date }}.</body></html>")
	html = t.render(Context({'current_date' : now}))
	return HttpResponse(html)

def hours_ahead(request, offset):
	offset = int(offset)
	later = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = "<html><body>In %s hour(s) it will be %s.</body></html>" % (offset, later)
	return HttpResponse(html)
"""

"""Method with a render_to_response, faster and more appropriate for this type
	of operation.

	PLEASE NOTE: 
	from django.shortcuts import render_to_response  NECESSARY!!

	HttpResponse and get_template CAN BE LEFT OUT
"""
def current_time(request):
	#now = datetime.datetime.now()
	#return render_to_response('mytemplate.html', {'current_date' : now})

	""" the mapping values in the dictionary can be done automatically by the method locals(), 
		here an example of the code changed.
		BENEFIT: less typing and less redundancy mapping variables
	"""
	current_date = datetime.datetime.now()
	return render_to_response('current_date.html', locals())

def hours_ahead(request, offset):
	hour_offset = int(offset)
	next_time = datetime.datetime.now() + datetime.timedelta(hours=hour_offset)
	return render_to_response('hours_ahead.html',locals())
