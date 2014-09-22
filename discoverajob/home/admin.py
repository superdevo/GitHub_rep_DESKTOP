from django.contrib import admin
from home.models import CustomUser, Countries, States, Cities, Post, PostReview


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Countries)
admin.site.register(States)
admin.site.register(Cities)

admin.site.register(Post)
admin.site.register(PostReview)
