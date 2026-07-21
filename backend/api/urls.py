from django.urls import path
from api import views

urlpatterns = [
    
    path("health/", views.health),
    path("demo/load/", views.load_demo),
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
    # delete selected files
    path("files/delete/", views.delete_files, name="delete-files"),
    # Delete every uploaded file in the current workspace
    path("files/delete-all/", views.delete_all, name="delete-all"),
]
