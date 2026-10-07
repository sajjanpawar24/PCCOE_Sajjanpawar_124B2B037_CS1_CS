"""Step 1: read the HLD PDF, split into chunks, embed, store in ChromaDB.
Run:  python Code/ingest.py
"""
import re

import chromadb
import pdfplumber
from sentence_transformers import SentenceTransformer

import config


def read_pages(pdf_path):
    """Return list of (page_number, section_title, text). Footer line is removed."""
    pages = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            lines = [l.strip() for l in (page.extract_text() or "").split("\n") if l.strip()]
            lines = [l for l in lines if not l.startswith("HLD-BCM-001 v1.0 | Synthetic")]
            if lines:
                pages.append((i, lines[0], lines))
    return pages


def chunk_page(page_no, title, lines, max_chars=config.CHUNK_CHARS):
    """Group lines into chunks up to max_chars. Each chunk keeps the section title for context."""
    chunks, current = [], []
    for line in lines[1:] if len(lines) > 1 else lines:
        if current and sum(len(x) + 1 for x in current) + len(line) > max_chars:
            chunks.append(current)
            current = current[-1:]          # overlap: repeat the last line
        current.append(line)
    if current:
        chunks.append(current)
    return [
        {"page": page_no, "section": title, "text": f"Section: {title}\n" + "\n".join(c)}
        for c in chunks
    ]


def build_index():
    pages = read_pages(config.PDF_PATH)
    chunks = []
    for page_no, title, lines in pages:
        chunks += chunk_page(page_no, title, lines)

    model = SentenceTransformer(config.EMBED_MODEL)
    embeddings = model.encode([c["text"] for c in chunks], normalize_embeddings=True).tolist()

    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR))
    try:
        client.delete_collection(config.COLLECTION)
    except Exception:
        pass
    col = client.create_collection(config.COLLECTION, metadata={"hnsw:space": "cosine"})
    col.add(
        ids=[f"p{c['page']}_c{i}" for i, c in enumerate(chunks)],
        documents=[c["text"] for c in chunks],
        embeddings=embeddings,
        metadatas=[{"page": c["page"], "section": c["section"]} for c in chunks],
    )
    print(f"Indexed {len(chunks)} chunks from {len(pages)} pages into '{config.COLLECTION}'")
    return len(chunks)


if __name__ == "__main__":
    build_index()
