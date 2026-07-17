from django.urls import path
from backend.api import views


urlpatterns = [
    path(
        "index/",
        views.index,
        name="index",
    ),
]