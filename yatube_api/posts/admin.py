from django.contrib import admin

from .models import Follow, Post, Group

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Group)
