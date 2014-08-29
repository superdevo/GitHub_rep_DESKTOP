from django.shortcuts import render, render_to_response
from chicagocrime.models import NewsItem

# Create your views here.
def index(request):
	return render_to_response('index.html')

def news_item(request, item):
	n = NewsItem.objects.get(pk=item)
	return render_to_response('detail.html', {'feed' : n })
