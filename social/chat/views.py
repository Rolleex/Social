from django.shortcuts import render, redirect
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User

from django.views import View

from account.models import Profile
from .models import ThreadModel, MessageModel
from .forms import ThreadForm, MessageForm


class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))

        message_list = MessageModel.objects.filter(Q(receiver_user=request.user) | Q(sender_user=request.user))
        context = {
            'threads': threads,
            'message_list':message_list,

        }

        return render(request, 'chat/inbox.html', context)


class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'chat/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')


class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'chat/thread.html', context)


class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message')
        )

        message.save()
        return redirect('thread', pk=pk)

def createtm(request, slug):

    username = Profile.objects.get(slug=slug)
    print(username )

    try:
        receiver = User.objects.get(username=username.user)
        if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
            thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
            return redirect('thread', pk=thread.pk)
        elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
            thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
            return redirect('thread', pk=thread.pk)
        else:

            thread = ThreadModel(
                user=request.user,
                receiver=receiver
            )
            thread.save()

            return redirect('thread', pk=thread.pk)
    except:
        return redirect('create-thread')