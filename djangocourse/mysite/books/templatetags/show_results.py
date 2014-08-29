from django import template
from books.models import Author

register = template.Library()

def show_books_for_author(author):
	a = Author.objects.get(first_name='Demi')
	books = a.book_set.all()
	return {'books' : books }

register.inclusion_tag('books_for_author.html')(show_books_for_author)