from django.urls import path
from .views import Index, Room, UserListView, ProfileView, ChatsView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path('chats/', ChatsView.as_view(), name='chats'),
    path("<str:room_name>/", Room.as_view(), name="room"),
    path("profile/", ProfileView.as_view(), name="profile"),
]