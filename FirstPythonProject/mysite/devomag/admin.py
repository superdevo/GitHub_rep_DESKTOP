from django.contrib import admin
from devomag.models import BlogEntry, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(BlogEntry)