"""Central settings. Change models or thresholds here only."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF_PATH = ROOT / "Input_Data" / "BCM_HLD_v1.0.pdf"
QUESTIONS_PATH = ROOT / "Input_Data" / "test_questions.json"
PROMPT_PATH = ROOT / "Model_Prompts_Config" / "system_prompt.txt"
RESULTS_DIR = ROOT / "Evaluation_Results"
CHROMA_DIR = ROOT / "Code" / "chroma_db"

# Embeddings (downloaded once from Hugging Face, then runs offline)
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "

# Vector store
COLLECTION = "bcm_hld"
TOP_K = 4
MAX_DISTANCE = 0.335  # if the best chunk is farther than this, answer "Not found". Tune after a retrieval-only run.

# Chunking
CHUNK_CHARS = 800

# LLM: local model served by Ollama (no external API)
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2:3b"
TEMPERATURE = 0.0
