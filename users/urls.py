from django.urls import path
from users.views import *

app_name = 'users'

urlpatterns = [
    ## template urls ##
    path('', homepage, name='homepage'),
    path('signup/', librarian_signup, name='librarian_signup'),
    path('login/', user_login, name='user_login'),


    ## api urls ##
    path('api/register/', register_user, name='register_user'),
    path('api/login/', login_user, name='login_user'),
    path('api/member/add/', add_member, name='add_member'),
    path("api/logout/", logout_user, name="logout_user")
]
