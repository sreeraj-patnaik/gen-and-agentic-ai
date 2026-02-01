from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector.django import CosineDistance

from .models import DocumentChunk


# Load embedding model (will download first time only)
MODEL = SentenceTransformer("all-MiniLM-L6-v2")


def load_pdf_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)


def split_text(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100,
    )
    return splitter.split_text(text)


def ingest_pdf(pdf_path: str, source_name="syllabus.pdf"):
    full_text = load_pdf_text(pdf_path)
    chunks = split_text(full_text)

    for chunk in chunks:
        emb = MODEL.encode(chunk).tolist()
        DocumentChunk.objects.create(
            text=chunk,
            embedding=emb,
            source=source_name
        )

    return len(chunks)


def search_similar(question: str, top_k=5):
    q_emb = MODEL.encode(question).tolist()

    return (
        DocumentChunk.objects
        .annotate(distance=CosineDistance("embedding", q_emb))
        .order_by("distance")[:top_k]
    )
