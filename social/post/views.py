from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from account.models import Follow, Profile
from post.models import Post, Like


@login_required
def viewpost(request):
    following_list = Follow.objects.filter(follower=request.user)
    feed = Post.objects.filter(author__in=following_list.values_list('following'))
    liked_post = Like.objects.filter(user=request.user)
    liked_post_list = liked_post.values_list('post', flat=True)
    return render(request, 'post/ViewPost.html', context={'feed': feed, 'liked_post_list': liked_post_list})


@login_required
def like(request, pk):
    post = Post.objects.get(pk=pk)
    already_like = Like.objects.filter(post=post, user=request.user)
    if not already_like:
        liked_post = Like(post=post, user=request.user)
        liked_post.save()
    return redirect(reverse('viewpost'))


@login_required
def unlike(request, pk):
    post = Post.objects.get(pk=pk)
    already_like = Like.objects.filter(post=post, user=request.user)
    already_like.delete()
    return redirect(reverse('viewpost'))
