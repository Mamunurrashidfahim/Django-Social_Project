
from App_Login.models import Follow, UserProfile
from django.contrib import admin
from django.contrib.auth.models import User

admin.site.register(UserProfile)
admin.site.register(Follow)