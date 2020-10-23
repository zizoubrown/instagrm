from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from post.models import Stream, Post, Tag, Likes
from post.forms import NewPostForm

#from comment.models import Comment
#from comment.forms import CommentForm

from django.contrib.auth.decorators import login_required

from django.urls import reverse
#from authy.models import Profile

# Create your views here.
