from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # all ragone endpoints + GUI go here
    path("", include("ragone.urls")),
]
