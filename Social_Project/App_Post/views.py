from django.urls import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from App_Login.models import Follow
from App_Post.models import Like, Post
@login_required
def home(request):
    if request.method =='GET':
        follwing_list = Follow.objects.filter(follower = request.user)
        posts = Post.objects.filter(author__in=follwing_list.values_list('following'))
        liked_post = Like.objects.filter(user=request.user)
        liked_post_list = liked_post.values_list('post',flat=True)
        search = request.GET.get('search','')
        result = User.objects.filter(username__icontains = search)
    return render(request,'App_Post/home.html',context={'search':search,'result':result,'posts':posts,'liked_post_list':liked_post_list})


@login_required
def liked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post, user=request.user)
    if not already_liked:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
        return HttpResponseRedirect(reverse('App_Post:home'))


@login_required
def unliked(request, pk):
    post = Post.objects.get(pk=pk)
    already_liked = Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('App_Post:home'))