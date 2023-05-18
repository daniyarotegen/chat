from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ChatRoom, Chat
from django.contrib.auth.models import User


class Index(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/index.html')


class ChatsView(LoginRequiredMixin, View):
    def get(self, request):
        chatrooms = ChatRoom.objects.filter(chat__user=request.user).distinct()
        chats_with_recipients = []
        for room in chatrooms:
            chat = room.chat_set.order_by('-timestamp').first()
            recipient_id = list(set(room.name.split("_")) - {str(request.user.id)})[0]
            recipient = User.objects.get(id=recipient_id)
            chats_with_recipients.append({'chat': chat, 'recipient': recipient})
        return render(request, 'chatrooms/chats.html', {'chats_with_recipients': chats_with_recipients})


class Room(LoginRequiredMixin, View):
    def get(self, request, room_name):
        recipient_user = User.objects.filter(username=room_name).first()
        if not recipient_user:
            return HttpResponse("User not found", status=404)

        room_name = "_".join(sorted([str(request.user.id), str(recipient_user.id)]))

        room = ChatRoom.objects.filter(name=room_name).first()
        chats = []

        if not room:
            room = ChatRoom(name=room_name)
            room.save()

        if room:
            chats = Chat.objects.filter(room=room)

        return render(request, 'chatrooms/room.html', {'room_name': room_name, 'chats': chats})


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.exclude(id=request.user.id)
        return render(request, 'chatrooms/user_list.html', {'users': users})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'chatrooms/profile.html')
