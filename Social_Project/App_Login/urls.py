from App_Login import views
from django.urls import path

app_name = "App_Login"

urlpatterns = [
    path ('signup/',views.sign_up, name='sign_up'),  
    path ('login/',views.login_page, name='login'), 
    path ('logout/',views.logout_user, name='logout'), 
    path ('edit/',views.edit_profile, name='edit'), 
    path ('edit_user/',views.user_change, name='edit_user'), 
    path ('password/',views.pass_change, name='pass_change'), 
    path ('profile/',views.profile, name='profile'), 
    path('user_other/<username>/', views.user_other, name='user_other'),
    path('follow/<username>/', views.follow, name='follow'),
    path('unfollow/<username>/', views.unfollow, name='unfollow'),
]