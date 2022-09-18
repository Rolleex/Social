import profile

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from .forms import RegisterForm, LoginForm, ProfileEditForm
from django.views.generic.detail import DetailView
from .models import Profile, Follow
from post.forms import PostForm


def register(request):
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            profile = Profile.objects.create(user=new_user)
            return redirect('login')

    else:
        user_form = RegisterForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':

        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if profile_form.is_valid():
            profile_form.save()

            return redirect('profile', request.user.profile.slug)
    else:
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request,
                      'account/create_profile.html',
                      {
                          'profile_form': profile_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile', request.user.profile.slug)
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def user(request, username):
    user_other = User.objects.get(username=username)
    already_followed = Follow.objects.filter(follower=request.user, following=user_other)
    if user == request.user:
        return redirect('profile')
    return render(request, 'account/user.html',
                  context={'user_other': user_other, 'already_followed': already_followed})


class ProfilePage(DetailView, CreateView):
    model = Profile
    template_name = 'account/profile.html'
    context_object_name = 'profile_page'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class Search(ListView):
    template_name = 'account/search.html'
    context_object_name = 'people'

    def get_queryset(self):
        return Profile.objects.filter(user__username__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context


@login_required
def follow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)

    if not already_followed:
        followed_user = Follow(follower=follower_user, following=following_user)
        followed_user.save()
    return redirect('user', following_user)


@login_required
def unfollow(request, username):
    following_user = User.objects.get(username=username)
    follower_user = request.user
    already_followed = Follow.objects.filter(follower=follower_user, following=following_user)
    already_followed.delete()
    return redirect(reverse('user', kwargs={'username': username}))
