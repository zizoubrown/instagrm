from django.urls import path
from .views import UserProfile, Signup, EditProfile, Inbox, UserSearch, Directs, NewConversation, SendDirect, ShowNOtifications, DeleteNotification
from .forms import SignupForm

from django.contrib.auth import views as authViews

urlpatterns = [
    path('profile/<username>/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'login'}, name='logout'),

    path('', Inbox, name='inbox'),
   	path('directs/<username>', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<username>', NewConversation, name='newconversation'),
   	path('send/', SendDirect, name='send_direct'),
	
	path('notification/', ShowNOtifications, name='show-notifications'),
   	path('<noti_id>/delete', DeleteNotification, name='delete-notification'),
]