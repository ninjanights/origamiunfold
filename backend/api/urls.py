from django.urls import path
from api import views

urlpatterns = [
    path(
        "upload/",
        views.upload,
        name="upload",
    ),
    path(
        "chat/",
        views.chat,
        name="chat",
    ),
    path("files/", views.files),
]
