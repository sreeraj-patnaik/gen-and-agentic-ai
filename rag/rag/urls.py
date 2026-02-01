from django.contrib import admin
from django.urls import path, include
from ragone.views import chat_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("ragone.urls")),
     path("chat/", chat_view),
]
