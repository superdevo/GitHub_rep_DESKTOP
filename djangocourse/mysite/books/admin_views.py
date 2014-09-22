import urllib2
import datetime 
from books.models import Book, Author, Publisher
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

def report(request):
	return render_to_response("admin/books/report.html",
		{'book_list' : Book.objects.all()},
		RequestContext(request, {}))
report = staff_member_required(report)

def add_by_isbn(request):
	if request.method == "POST":
		isbn = request.POST.get('isbn', False)
		response = urllib2.urlopen('http://isbn.nu/' + isbn)
		html = response.read()
		content_title_split = html.split("<title>", 1)
		title = content_title_split[1].split("</title>", 1)[0]
		author = Author.objects.get(first_name='Demi')
		publisher = Publisher.objects.get(pk=1)
		num_pages = 93
		pub_date = datetime.datetime.now()

		try:
			new_book = Book.objects.get(title=title)
		except Book.DoesNotExist:
			new_book = Book(title=title, publisher=publisher,publication_date=pub_date, num_pages=num_pages)
			new_book.save()
			new_book.authors.add(author)


		return HttpResponseRedirect("/admin/books/report/")	
	else:
		return render_to_response("admin/books/book/add_from_isbn.html",
			RequestContext(request))