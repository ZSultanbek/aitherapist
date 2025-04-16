from django.urls import path
from .views import chat, home

urlpatterns = [
    path("chat/", chat, name="chat"),
    path("", home, name="home")
]
