"""Step 2: retrieve + answer with citations.
Uses a local Ollama model. If Ollama is not running, falls back to 'extractive' mode
(returns the best matching passage with its page), so the app never crashes in a demo.
"""
import re
from functools import lru_cache

import chromadb
import requests
from sentence_transformers import SentenceTransformer

import config

NOT_FOUND = "Not found in the document."


@lru_cache(maxsize=1)
def _resources():
    model = SentenceTransformer(config.EMBED_MODEL)
    col = chromadb.PersistentClient(path=str(config.CHROMA_DIR)).get_collection(config.COLLECTION)
    prompt = config.PROMPT_PATH.read_text(encoding="utf-8")
    return model, col, prompt


def retrieve(question, k=config.TOP_K):
    model, col, _ = _resources()
    emb = model.encode([config.QUERY_PREFIX + question], normalize_embeddings=True).tolist()
    res = col.query(query_embeddings=emb, n_results=k)
    return [
        {"text": d, "page": m["page"], "section": m["section"], "distance": float(dist)}
        for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def _call_ollama(system_prompt, context, question):
    payload = {
        "model": config.OLLAMA_MODEL,
        "stream": False,
        "options": {"temperature": config.TEMPERATURE},
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    }
    r = requests.post(config.OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    return r.json()["message"]["content"].strip()


def cited_pages(text):
    return sorted({int(n) for n in re.findall(r"\[?Page\s*(\d+)\]?", text, flags=re.I)})


def answer(question, use_llm=True):
    hits = retrieve(question)
    top = hits[0]
    result = {"question": question, "retrieved_pages": [h["page"] for h in hits],
              "top_distance": round(top["distance"], 3), "hits": hits}

    if top["distance"] > config.MAX_DISTANCE:
        result.update(answer=NOT_FOUND, mode="threshold-refusal", cited=[])
        return result

    context = "\n\n".join(f"[Page {h['page']}] {h['text']}" for h in hits)
    if use_llm:
        try:
            text = _call_ollama(_resources()[2], context, question)
            result.update(answer=text, mode=f"llm:{config.OLLAMA_MODEL}", cited=cited_pages(text))
            return result
        except Exception as e:  # Ollama not running etc.
            result["llm_error"] = str(e)[:120]

    text = f"{top['text']} [Page {top['page']}]"
    result.update(answer=text, mode="extractive", cited=[top["page"]])
    return result
