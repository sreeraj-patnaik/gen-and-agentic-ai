from sentence_transformers import SentenceTransformer
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pgvector.django import CosineDistance

from .models import DocumentChunk


MODEL = None

def get_model():
    global MODEL
    if MODEL is None:
        MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return MODEL


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

    model = get_model()

    for chunk in chunks:
        emb = model.encode(chunk).tolist()
        DocumentChunk.objects.create(
            text=chunk,
            embedding=emb,
            source=source_name
        )

    return len(chunks)


def search_similar(question: str, top_k=5):
    model = get_model()
    q_emb = model.encode(question).tolist()

    return (
        DocumentChunk.objects
        .annotate(distance=CosineDistance("embedding", q_emb))
        .order_by("distance")[:top_k]
    )
