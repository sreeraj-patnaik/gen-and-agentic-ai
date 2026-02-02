from django.urls import path
from .views import ingest_view, ask_view, chat_view, chat_page

urlpatterns = [
    # GUI Home
    path("", chat_page),

    # API endpoints
    path("api/ingest/", ingest_view),
    path("api/ask/", ask_view),
    path("api/chat/", chat_view),
]