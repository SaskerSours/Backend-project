from django.contrib import admin

# Register your models here.
from .models import Contact, Post, Group, Comments

admin.site.register(Contact)
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comments)
