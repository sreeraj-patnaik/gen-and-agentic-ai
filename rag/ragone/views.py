from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os

from .rag_engine import ingest_pdf, search_similar
from .models import DocumentChunk

from .mistral_client import mistral_answer

@api_view(["POST"])
def ingest_view(request):
    # optional: clear previous chunks to avoid duplicates
    DocumentChunk.objects.all().delete()

    pdf_path = os.path.join(settings.BASE_DIR, "data", "syllabus.pdf")

    if not os.path.exists(pdf_path):
        return Response(
            {"error": "PDF not found. Put it in rag/data/syllabus.pdf"},
            status=400
        )

    count = ingest_pdf(pdf_path, source_name="syllabus.pdf")

    return Response({
        "message": "Ingested successfully ✅",
        "chunks_created": count
    })


@api_view(["POST"])
def ask_view(request):
    question = request.data.get("question")

    if not question:
        return Response({"error": "question is required"}, status=400)

    results = search_similar(question, top_k=5)

    return Response({
        "question": question,
        "retrieved_chunks": [r.text for r in results],
    })

@api_view(["POST"])
def chat_view(request):
    question = request.data.get("question")

    if not question:
        return Response({"error": "question is required"}, status=400)

    results = search_similar(question, top_k=5)

    context = "\n\n---\n\n".join([r.text for r in results])

    answer = mistral_answer(question, context)

    return Response({
        "question": question,
        "answer": answer,
        "chunks_used": len(results),
    })
