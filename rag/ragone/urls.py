from django.urls import path
from .views import ingest_view, ask_view

urlpatterns = [
    path("ingest/", ingest_view),
    path("ask/", ask_view),
]
