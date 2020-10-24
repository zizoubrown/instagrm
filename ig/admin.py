from django.contrib import admin
from .models import Profile, Comment, Message, Notification

admin.site.site_header = "Instagram Admin"
admin.site.site_title = "Instagram Admin Area"
admin.site.index_title = "Welcome to instagram admin"

# Register your models here.
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)