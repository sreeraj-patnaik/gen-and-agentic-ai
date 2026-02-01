from django.db import models
from pgvector.django import VectorField


class DocumentChunk(models.Model):
    text = models.TextField()
    embedding = VectorField(dimensions=384)  # MiniLM produces 384-d vectors
    source = models.CharField(max_length=255, default="syllabus.pdf")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} | {self.id}"
