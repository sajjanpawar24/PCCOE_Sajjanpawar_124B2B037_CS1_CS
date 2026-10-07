"""One command for the whole pipeline: index -> evaluate -> build PDFs.
Run:  python Code/run_all.py        (add --no-llm if Ollama is not available)
"""
import sys

import build_documents
import evaluate
import ingest

ingest.build_index()
evaluate.main(use_llm="--no-llm" not in sys.argv)
build_documents.synopsis()
build_documents.declaration()
build_documents.report()
print("\nALL DONE. Now: record video, sign pages, zip the folder.")
