# AUTOSAR HLD Document Analysis Assistant using RAG with Citations

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.65.0-red.svg)](https://streamlit.io)

> **Retrieval-Augmented Generation (RAG) system for answering questions about AUTOSAR High-Level Design documents with mandatory page citations.**

**Student:** Sajjan Pawar | **PRN:** 124B2B037 | **Division:** CS  
**Faculty Guide:** Ms. Harsha Talele  
**Institution:** Pimpri Chinchwad College of Engineering (PCCOE), Pune  
**Project:** TATA Technologies Tech Pulse FY-26 AI/ML Capstone Project

---

## 🎯 Project Overview

AUTOSAR High-Level Design (HLD) documents are typically 50-200 page PDFs containing component architectures, interface specifications, CAN signals, and functional flows. Engineers waste significant time searching for specific details. This project builds a **RAG-based assistant** that:

✅ Answers questions using **only** information from the document  
✅ Provides **mandatory [Page N] citations** for every answer  
✅ **Refuses safely** with "Not found in the document" when information is missing  
✅ Shows **retrieved evidence** for user verification  

---

## 🏗️ Architecture

```
User Question
    ↓
BGE-small-en-v1.5 Embeddings (384-dim)
    ↓
ChromaDB Retrieval (Top-4, Cosine Distance)
    ↓
Threshold Check (distance > 0.335?)
    ├─ Yes → Refuse: "Not found in the document"
    └─ No  → LLM Generation (llama3.2:3b via Ollama)
              ↓
         Answer + [Page N] Citations
```

**Key Components:**
- **Embedding Model:** BAAI/bge-small-en-v1.5 (Hugging Face, runs offline)
- **Vector Store:** ChromaDB with persistent storage, cosine distance
- **LLM:** llama3.2:3b via Ollama (local, temperature 0.0)
- **UI:** Streamlit with interactive Q&A and evidence display
- **Knowledge Base:** Synthetic 14-page BCM HLD (no real company data)

---

## 📊 Evaluation Results

**Test Set:** 30 questions (28 answerable, 2 unanswerable)  
**Evaluation Mode:** Extractive (retrieval + best passage) — LLM code implemented but not evaluated due to Ollama unavailability

| Metric | Score |
|--------|-------|
| **Retrieval Hit Rate** | 96.4% (27/28 questions retrieved expected page) |
| **Answer Accuracy** | 78.6% (22/28 questions had all required keywords) |
| **Citation Accuracy** | 78.6% (22/28 questions cited expected page) |
| **Correct Refusal Rate** | 100.0% (2/2 unanswerable questions refused) |

**Failure Analysis:** 6 questions incorrect
- 4 questions refused by threshold (distances 0.343-0.407, valid answers existed)
- 1 question retrieved correct page but keyword missing in extracted passage
- 1 question retrieved wrong page

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.10+
- Virtual environment (recommended)
- Ollama (optional, for LLM mode)

### **Installation**

```bash
# Clone repository
git clone https://github.com/sajjanpawar24/PCCOE_Sajjanpawar_124B2B037_CS1_CS.git
cd PCCOE_Sajjanpawar_124B2B037_CS1_CS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r Code/requirements.txt
```

### **Optional: Install Ollama for LLM Mode**
```bash
# Install Ollama from https://ollama.com
# Pull the model
ollama pull llama3.2:3b
```

### **Run the Application**

```bash
# Step 1: Build vector index (one-time, downloads BGE model ~133MB)
python Code/ingest.py

# Step 2: Run evaluation (optional)
python Code/evaluate.py --no-llm

# Step 3: Start Streamlit app
streamlit run Code/app.py
```

Open your browser at **http://localhost:8501**

---

## 💡 Usage Examples

### **Example 1: Successful Answer with Citation**
**Question:** "What does DoorLockManager do when CrashDetected is set?"

**Answer:**  
> DoorLockManager locks and unlocks the four doors. When the signal CrashDetected is set to 1 by the airbag control unit, DoorLockManager unlocks all doors within 100 ms. **[Page 4]**

**Retrieved Pages:** [4, 10, 12, 13]  
**Top Distance:** 0.197

---

### **Example 2: Correct Refusal**
**Question:** "What is the current limit of the wiper motor?"

**Answer:**  
> Not found in the document.

**Reason:** Wipers are out of scope (distance 0.35 > threshold 0.335)

---

## 📁 Project Structure

```
├── Code/
│   ├── app.py                    # Streamlit UI
│   ├── ingest.py                 # PDF → ChromaDB indexing
│   ├── rag.py                    # RAG pipeline (retrieve + generate)
│   ├── evaluate.py               # Evaluation on 30-question test set
│   ├── config.py                 # Central configuration
│   ├── build_documents.py        # Generate PCCOE PDFs
│   ├── build_tata_docs.py        # Generate Tata PDFs
│   ├── generate_hld.py           # Create synthetic BCM HLD
│   ├── run_all.py                # One-command pipeline
│   └── requirements.txt          # Python dependencies
├── Input_Data/
│   ├── BCM_HLD_v1.0.pdf          # Synthetic 14-page AUTOSAR HLD
│   └── test_questions.json       # 30 ground-truth questions
├── Evaluation_Results/
│   ├── results.csv               # Per-question results
│   ├── summary.json              # Aggregated metrics
│   └── sample_outputs.md         # Sample Q&A outputs
├── Documentation/
│   ├── README_RUN_STEPS.md       # Detailed run instructions
│   ├── Technical_Report.pdf      # PCCOE technical report
│   ├── Video_Script_5to10min.md  # Video recording script
│   └── student_info.json         # Student details
├── Synopsis/
│   └── TATA_Synopsis.pdf         # Project synopsis
├── Tata_Documents/
│   └── TATA_TechnicalReport.pdf  # Tata Technologies report
├── Declarations/
│   └── Student_Declaration.pdf   # Student declaration
├── Model_Prompts_Config/
│   └── system_prompt.txt         # LLM system prompt
└── .gitignore                    # Excludes venv, cache, chroma_db
```

---

## 🔧 Configuration

Edit `Code/config.py` to customize:

```python
# Chunking
CHUNK_CHARS = 800                 # Max characters per chunk

# Retrieval
TOP_K = 4                         # Number of chunks to retrieve
MAX_DISTANCE = 0.335              # Refusal threshold (cosine distance)

# LLM (Ollama)
OLLAMA_MODEL = "llama3.2:3b"
OLLAMA_URL = "http://localhost:11434/api/chat"
TEMPERATURE = 0.0                 # Deterministic answers

# Embeddings
EMBED_MODEL = "BAAI/bge-small-en-v1.5"
```

---

## 📈 Key Features

### **1. Section-Aware Chunking**
Section headers preserved in chunks for better context:
```
"Section: 3.1 DoorLockManager
DoorLockManager locks and unlocks the four doors..."
```

### **2. Distance-Based Refusal**
Deterministic rule prevents hallucination:
- If `top_distance > 0.335` → Refuse ("Not found in the document")
- Achieves **100% correct refusal rate** on test set

### **3. Citation Verification UI**
Streamlit app shows:
- Answer with [Page N] citations
- All 4 retrieved chunks with distances
- Expandable "Retrieved evidence" for verification

### **4. Dual-Mode Evaluation**
- **Extractive mode (`--no-llm`):** Retrieval + best passage (fast)
- **LLM mode:** Full RAG pipeline with generation (requires Ollama)

---

## 🛡️ Responsible AI Measures

| Area | Measure |
|------|---------|
| **Grounding & Citations** | Mandatory [Page N] citations, retrieved evidence shown in UI, regex verification |
| **Privacy** | Synthetic data only, local execution, no data collection, no cloud APIs |
| **Security** | Localhost only, no authentication (demo), input validation, no code injection risk |
| **Human Oversight** | UI disclaimer: "Review every answer against the cited page", limitations documented |

---

## ⚠️ Known Limitations

1. **Single document:** Works on one 14-page PDF (synthetic data), no multi-document support
2. **Text only:** No OCR, no diagram understanding, text and tables only
3. **Threshold tradeoff:** 4 valid questions refused due to high embedding distances (0.343-0.407)
4. **Keyword evaluation:** Marks correct paraphrases as wrong (e.g., "five" vs "5")
5. **Test set = tuning set:** Refusal threshold (0.335) tuned on same 30 questions, making 100% refusal rate optimistic
6. **Small local model:** llama3.2:3b may miss multi-part answers or cite wrong pages

---

## 🚧 Future Work

- [ ] Independent validation set for unbiased threshold tuning
- [ ] Full LLM evaluation (extractive mode only tested)
- [ ] Semantic answer scoring (replace keyword matching)
- [ ] Multi-document knowledge base
- [ ] Revision comparison across document versions
- [ ] Graph relationships (Neo4j for component-interface-signal graphs)
- [ ] Production deployment (FastAPI, Docker, PostgreSQL)
- [ ] Role-based access control

---

## 🛠️ Technologies Used

| Category | Technology |
|----------|-----------|
| **Embeddings** | BAAI/bge-small-en-v1.5 (Hugging Face) |
| **Vector Store** | ChromaDB 1.5.9 |
| **LLM** | llama3.2:3b (Ollama) |
| **PDF Processing** | pdfplumber |
| **UI** | Streamlit 1.65.0 |
| **Document Generation** | ReportLab |
| **Evaluation** | Custom keyword-based metrics |

---

## 📄 License

This project is submitted as part of the TATA Technologies Tech Pulse FY-26 AI/ML Capstone Project and contains synthetic data only.

---

## 🙏 Acknowledgments

- **Faculty Guide:** Ms. Harsha Talele (PCCOE)
- **TATA Technologies** for the capstone project opportunity
- **Hugging Face** for BGE embeddings
- **Ollama** for local LLM inference
- **Streamlit** for rapid UI development

---

## 📞 Contact

**Sajjan Pawar**  
PRN: 124B2B037  
Division: CS  
Pimpri Chinchwad College of Engineering (PCCOE), Pune

---

## 📊 Citations

```bibtex
@misc{pccoe2026autosar,
  title={AUTOSAR HLD Document Analysis Assistant using RAG with Citations},
  author={Pawar, Sajjan},
  year={2026},
  institution={Pimpri Chinchwad College of Engineering},
  note={TATA Technologies Tech Pulse FY-26 AI/ML Capstone Project}
}
```

---

**⭐ If you find this project useful, please star the repository!**
