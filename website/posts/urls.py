from django.urls import path, re_path
from . import views

urlpatterns = [
    path("personal/", views.myPosts),
    path("new/", views.createpost),
    path("edit/<str:id>/", views.createpost),
    path("delete/<str:id>/", views.deletePost),
    path("subscribe/<str:post>/", views.subscribe),
    path("image/address/", views.serve_image),
    path("<str:id>/<str:lang>", views.postDetails),
]
