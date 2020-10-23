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
@login_required
def index(request):
	posts = Post.objects.all()
	template = loader.get_template('index.html')
	context = {'post_items': posts}

	return HttpResponse(template.render(context, request))

@login_required
def timeline(request):
	user = request.user
	posts = Stream.objects.filter(user=user)
	users = User.objects.all()

	group_ids = []

	for post in posts:
		group_ids.append(post.post_id)
		
	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')		

	template = loader.get_template('timeline.html')

	context = {
	'post_items': post_items,
	'users':users,

	}

	return HttpResponse(template.render(context, request))