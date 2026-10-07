# AUTOSAR HLD Document Analysis Assistant - Run Steps

## What it does
Answers questions about a (synthetic) AUTOSAR-style High-Level Design PDF. Every answer is built only from retrieved pages and ends with a page citation. If the answer is not in the document, it says "Not found in the document."

## Pipeline
PDF -> text per page (pdfplumber) -> section chunks -> BGE embeddings -> ChromaDB -> top-4 retrieval -> local LLM (Ollama) -> answer + [Page N] citations -> Streamlit UI

## Setup (once)
1. Python 3.10+ and a virtual environment.
2. `pip install -r Code/requirements.txt`
3. Install Ollama from ollama.com, then run: `ollama pull llama3.2:3b`
4. Start Ollama (it runs in the background after install).

## Run (from the project root)
1. `python Code/generate_hld.py`   (only if Input_Data/BCM_HLD_v1.0.pdf is missing)
2. `python Code/ingest.py`         (builds the vector index)
3. `python Code/evaluate.py --no-llm`   (quick check, retrieval only)
4. `python Code/evaluate.py`       (full evaluation, saves to Evaluation_Results/)
5. `streamlit run Code/app.py`     (demo UI)

## External dependencies (declare these)
- Hugging Face download of the embedding model `BAAI/bge-small-en-v1.5`: needs internet ONCE, then works offline.
- LLM `llama3.2:3b` runs locally through Ollama: needs internet ONCE to download. No cloud API is used at run time.
- No other external API.

## Known limitations (use in the report)
- One synthetic document, 14 pages, text and simple tables only. No diagrams, no OCR.
- Small local model can miss multi-part answers or add wrong citations.
- Distance threshold for "Not found" is set by hand (config.py, MAX_DISTANCE).
- Not built (future work): revision comparison, graph relationships, role-based access, FastAPI, PostgreSQL, Neo4j.

## Fast path (one command)
1. Edit Documentation/student_info.json (name, PRN, division, faculty).
2. `python Code/run_all.py`  (add `--no-llm` if Ollama is not available). It builds the index, runs the evaluation and regenerates Synopsis, Declaration and Technical Report PDFs with real numbers.
3. Print Synopsis/Project_Synopsis.pdf and Declarations/Student_Declaration.pdf, sign, scan or photograph, and save the signed copies next to them.
4. Record the video using Documentation/Video_Script_5to10min.md and save it in Video/.
5. Zip the whole folder.
