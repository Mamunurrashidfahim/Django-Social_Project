from App_Post.forms import PostForm
from django.contrib.auth.models import User
from App_Login.models import Follow, UserProfile
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render
from App_Login.forms import CreateNewUser, EditProfile, LoginUser, ProfileChangeForm
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def sign_up(request):
    form = CreateNewUser
    registered = False
    if request.method == 'POST':
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user = form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_Login:login'))
    return  render(request,'App_Login/signup.html',context={'form': form})


def login_page(request):
    form = LoginUser()
    if request.method =='POST':
        form = LoginUser(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request,'App_Login/login.html',context={'form':form})


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_Login:login'))


@login_required
def profile(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('App_Post:home'))
    return render(request,'App_Login/profile.html',context={'form':form})

@login_required
def edit_profile(reguest):
    current_user =UserProfile.objects.get(user=reguest.user)
    form = EditProfile(instance=current_user)
    if reguest.method == 'POST':
        form = EditProfile(reguest.POST,reguest.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('App_Login:profile'))
            form = EditProfile(instance=current_user)
    return render(reguest,'App_Login/edit.html',context={'form':form})


@login_required
def user_change(request):
    current_user = request.user
    form = ProfileChangeForm(instance=current_user)
    if request.method == 'POST':
        form = ProfileChangeForm(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            form = ProfileChangeForm(instance=current_user)
            return HttpResponseRedirect(reverse('App_Login:profile'))
    return render(request, 'App_Login/edit_user.html', context={'form': form})


@login_required
def pass_change(request):
    current_user = request.user
    changed = False
    form = PasswordChangeForm(current_user)
    if request.method == 'POST':
        form = PasswordChangeForm(current_user, data=request.POST)
        if form.is_valid():
            form.save()
            changed = True
    return render(request, 'App_Login/pass_change.html', context={'form': form, 'changed': changed})


@login_required
def user_other(request,username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(following=user_other, follower=request.user)
    if user_other == request.user:
        return HttpResponseRedirect(reverse('App_Login:profile'))
    
    return render(request,'App_Login/user_other.html',context={'user_other':user_other,'already_followed':already_followed})


@login_required
def follow(request,username):
    following_user= User.objects.get(username=username)
    follower_user= request.user
    already_followed = Follow.objects.filter(following=following_user,follower=follower_user)
    if not already_followed:
        followed_user = Follow(following= following_user,follower = follower_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_Login:user_other',kwargs={'username':username}))

@login_required
def unfollow(request,username):
    following_user= User.objects.get(username=username)
    follower_user= request.user
    already_followed = Follow.objects.filter(following=following_user,follower=follower_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_Login:user_other',kwargs={'username':username}))