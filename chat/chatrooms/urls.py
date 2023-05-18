from django.urls import path
from .views import Index, Room, UserListView

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("users/", UserListView.as_view(), name="user-list"),
    path("<str:room_name>/", Room.as_view(), name="room"),
]