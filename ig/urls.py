from django.urls import path
from .views import UserProfile, Signup, PasswordChange, PasswordChangeDone, EditProfile, Inbox, UserSearch, Directs, NewConversation, SendDirect

from django.contrib.auth import views as authViews

urlpatterns = [
    path('profile/<username>/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
   	path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'login'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('', Inbox, name='inbox'),
   	path('directs/<username>', Directs, name='directs'),
   	path('new/', UserSearch, name='usersearch'),
   	path('new/<username>', NewConversation, name='newconversation'),
   	path('send/', SendDirect, name='send_direct'),
]