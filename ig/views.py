from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .forms import SignupForm, ChangePasswordForm, EditProfileForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, logout

from .models import Profile, Message
from post.models import Post, Follow, Stream
from django.db import transaction
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse

from django.core.paginator import Paginator

from django.urls import resolve

from django.db.models import Q

# Create your views here.
def UserProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#follow status
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
		'follow_status':follow_status,
		'url_name':url_name,
	}

	return HttpResponse(template.render(context, request))

def UserProfileFavorites(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	posts = profile.favorites.all()

	#Profile info box
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	#Pagination
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	context = {
		'posts': posts_paginator,
		'profile':profile,
		'following_count':following_count,
		'followers_count':followers_count,
		'posts_count':posts_count,
	}

	return HttpResponse(template.render(context, request))

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    context = {
		'form':form,
	}
    return render(request, 'login.html',context)

def logout(request):
    logout(request)
    return redirect('login')

def Signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('login')
	else:
		form = SignupForm()
	
	context = {
		'form':form,
	}

	return render(request, 'signup.html', context)

@login_required
def EditProfile(request, username):
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	BASE_WIDTH = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return HttpResponseRedirect(reverse('profile', args=[username]))
	else:
		form = EditProfileForm()

	context = {
		'form':form,
	}

	return render(request, 'edit_profile.html', context)

@login_required
def follow(request, username, option):
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			 posts = Post.objects.all().filter(user=following)[:25]

			 with transaction.atomic():
			 	for post in posts:
			 		stream = Stream(post=post, user=request.user, date=post.posted, following=following)
			 		stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))
	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))

@login_required
def Inbox(request):
	users = User.objects.all()
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		'users':users,
		}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))

@login_required
def UserSearch(request):
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		#Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('direct/search_user.html')
	
	return HttpResponse(template.render(context, request))

@login_required
def Directs(request, username):
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct':active_direct,
		'users':users,
	}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))

@login_required
def NewConversation(request, username):
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('usersearch')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')

@login_required
def SendDirect(request):
	# to_user = User.objects.get(username=username)
    
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	else:
		HttpResponseBadRequest()
		
def checkDirects(request):
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count':directs_count}
