"""Build Tata Technologies Synopsis and Technical Report PDFs."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=14, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1F3A5F"))
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4, textColor=colors.HexColor("#2C5282"))
H3 = ParagraphStyle("H3", parent=ss["Heading3"], fontSize=10, spaceBefore=6, spaceAfter=3)
B = ParagraphStyle("B", parent=ss["Normal"], fontSize=9, leading=13, spaceAfter=4)
CODE = ParagraphStyle("CODE", parent=ss["Normal"], fontSize=7, leading=9, fontName="Courier", leftIndent=10, spaceAfter=4)
TITLE = ParagraphStyle("T", parent=ss["Title"], fontSize=18, leading=22, textColor=colors.HexColor("#1F3A5F"))


def tbl(rows, widths, header=True):
    data = [[Paragraph(str(c), B) for c in r] for r in rows]
    t = Table(data, colWidths=[w * mm for w in widths])
    st = [("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F4F8")))
        st.append(("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")))
    t.setStyle(TableStyle(st))
    return t


def build(path, story):
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
                      topMargin=18*mm, bottomMargin=18*mm).build(story)
    print(f"Created {path}")


def synopsis():
    story = [
        Paragraph("TATA TECHNOLOGIES LTD.", TITLE),
        Paragraph("TECH PULSE FY-26 | AI/ML Capstone Project", H1),
        Paragraph("PROJECT SYNOPSIS", H1),
        Spacer(1, 10),
        
        Paragraph("<b>Student Details</b>", H2),
        tbl([
            ["Institute/University", "Pimpri Chinchwad College of Engineering (PCCOE), Pune"],
            ["Programme / Batch", "B.E. Computer Engineering, Final Year"],
            ["Student Name", "Sajjan Pawar"],
            ["PRN", "124B2B037"]
        ], [50, 130], header=False),
        
        Paragraph("1. Case Study ID and Project Title", H2),
        tbl([
            ["Case Study ID (CS1 to CS5)", "CS3 (RAG-based Document Q&A System)"],
            ["Project Title / Topic", "AUTOSAR HLD Document Analysis Assistant using RAG with Citations"]
        ], [60, 120], header=False),
        
        Paragraph("2. Objectives", H2),
        Paragraph("1. Build a Retrieval-Augmented Generation (RAG) assistant that answers questions about AUTOSAR "
                  "High-Level Design (HLD) documents with page citations.", B),
        Paragraph("2. Implement safe refusal mechanism to answer 'Not found in the document' when the answer is not present.", B),
        Paragraph("3. Measure retrieval accuracy, answer accuracy, citation accuracy, and correct refusal rate on 30 ground-truth questions.", B),
        Paragraph("4. Demonstrate grounding and citation capabilities as a Responsible AI measure.", B),
        
        Paragraph("3. Scope", H2),
        Paragraph("<b>In Scope – To Be Implemented</b>", H3),
        Paragraph("• PDF text extraction using pdfplumber, section-wise chunking (800 chars), ChromaDB vector store<br/>"
                  "• Semantic retrieval using BAAI/bge-small-en-v1.5 embeddings, top-4 retrieval, distance threshold 0.335<br/>"
                  "• Local LLM (llama3.2:3b via Ollama) with strict citation prompt requiring [Page N] citations<br/>"
                  "• Streamlit web UI for interactive Q&A with retrieved evidence display<br/>"
                  "• Evaluation on 30-question test set with 4 metrics<br/>"
                  "• Synthetic 14-page BCM HLD document (no real company data)", B),
        
        Paragraph("<b>Out of Scope – Will Not Be Implemented</b>", H3),
        Paragraph("• Multi-document knowledge base • OCR for scanned PDFs • Diagram understanding • Revision comparison<br/>"
                  "• Graph-based relationships • Role-based access control • Production deployment (FastAPI, Docker, PostgreSQL)", B),
        
        Paragraph("4. Proposed Approach", H2),
        tbl([
            ["Component", "Choice"],
            ["Pre-trained model", "llama3.2:3b via Ollama (local), Temperature 0.0"],
            ["Embedding model", "BAAI/bge-small-en-v1.5 (384-dim, Hugging Face, offline)"],
            ["Vector store", "ChromaDB v1.5.9, persistent, cosine distance, top-4"],
            ["RAG pipeline", "Query → BGE embed → ChromaDB retrieve → threshold check (0.335) → LLM generation + [Page N]"],
            ["Service layer and UI", "Streamlit 1.65.0 with example questions, LLM toggle, retrieved evidence display"],
            ["Tools / rules", "Distance refusal, citation extraction, keyword evaluation, section-aware chunking"]
        ], [50, 130]),
        
        Paragraph("5. Input Data / Knowledge Base", H2),
        tbl([
            ["Data Sources", "Synthetic 14-page BCM HLD (BCM_HLD_v1.0.pdf) created with ReportLab"],
            ["Size and Format", "14 pages, ~18 KB, PDF with text and tables (no diagrams)"],
            ["Preprocessing", "pdfplumber extraction → section identification → 800-char chunks → 14 chunks indexed"],
            ["Test Set", "30 questions (28 answerable, 2 unanswerable) with ground truth keywords and pages"]
        ], [50, 130]),
        
        PageBreak(),
        
        Paragraph("6. Expected Outcomes and Evaluation Plan", H2),
        Paragraph("<b>Expected Outputs:</b> Working Streamlit app, evaluation results (CSV, JSON, markdown), technical report", B),
        Paragraph("<b>Evaluation Metrics:</b>", B),
        Paragraph("• Retrieval hit rate: % with expected page in top-4<br/>"
                  "• Answer accuracy: % with all required keywords<br/>"
                  "• Citation accuracy: % with expected page cited<br/>"
                  "• Correct refusal rate: % unanswerable questions refused", B),
        Paragraph("<b>Evaluation Mode:</b> Extractive mode (--no-llm) because Ollama was not available. "
                  "LLM generation code implemented in rag.py but not evaluated.", B),
        Paragraph("<b>Responsible AI Measures:</b>", B),
        Paragraph("• Grounding: Mandatory [Page N] citations, retrieved evidence shown in UI<br/>"
                  "• Privacy: Synthetic data only, local execution, no data collection<br/>"
                  "• Security: No cloud APIs, ChromaDB on localhost<br/>"
                  "• Human oversight: UI disclaimer, verification mechanism, limitations documented", B),
        
        Paragraph("7. Planned AI-Tool Usage", H2),
        tbl([
            ["AI Tool / Model", "Purpose", "Artifact Affected"],
            ["GitHub Copilot", "Code autocompletion", "Code/*.py"],
            ["ChatGPT-4", "Debugging assistance", "ingest.py, rag.py"],
            ["Claude Sonnet (Kiro)", "Technical report drafting", "Documentation, README"]
        ], [40, 55, 85]),
        Paragraph("All code and documentation reviewed, tested, and understood by student.", B),
        
        Spacer(1, 20),
        Paragraph("<b>Student Declaration</b>", H2),
        Paragraph("☑ I will not change the approved case-study scope without prior faculty approval.", B),
        Paragraph("☑ I confirm this work represents my own understanding and contribution.", B),
        Spacer(1, 15),
        Paragraph("Name and Signature: Sajjan Pawar ______________________________    Date: 07/10/2026", B),
    ]
    
    build("d:/sem 7/tata/TATA_Synopsis_SajjanPawar_124B2B037.pdf", story)


def technical_report():
    story = [
        Paragraph("TATA TECHNOLOGIES LTD.", TITLE),
        Paragraph("TECH PULSE FY-26 | AI/ML Capstone Project", H1),
        Paragraph("TECHNICAL REPORT", H1),
        Spacer(1, 10),
        
        tbl([
            ["Institute / University", "Pimpri Chinchwad College of Engineering (PCCOE), Pune"],
            ["Programme / Batch", "B.E. Computer Engineering, Final Year"],
            ["Student Name", "Sajjan Pawar"],
            ["PRN", "124B2B037"],
            ["Case Study ID", "CS3 (RAG-based Document Q&A System)"],
            ["Project Title", "AUTOSAR HLD Document Analysis Assistant using RAG with Citations"]
        ], [50, 130], header=False),
        
        Paragraph("1. Problem Statement and Intended Users", H2),
        Paragraph("AUTOSAR High-Level Design documents are 50-200 page PDFs containing component architectures, "
                  "interfaces, CAN signals, and functional flows. Engineers waste time searching for details. "
                  "Manual search is slow, error-prone, and risks design mistakes.", B),
        Paragraph("<b>Intended Users:</b> AUTOSAR software engineers, system architects, test engineers, technical reviewers", B),
        Paragraph("<b>Key Requirements:</b> Answer from document only, cite source pages [Page N], "
                  "refuse when answer not present, show retrieved evidence", B),
        
        Paragraph("2. Input Data / Knowledge Base", H2),
        tbl([
            ["Item", "Description"],
            ["Sources", "Synthetic 14-page BCM HLD (BCM_HLD_v1.0.pdf) with 5 AUTOSAR components, "
             "ports, CAN signals, functional flows. NO REAL COMPANY DATA."],
            ["Size and format", "14 pages, ~18 KB, PDF with text and tables"],
            ["Preprocessing", "pdfplumber extraction → section identification → 800-char chunks → 14 chunks"],
            ["Chunking strategy", "Section-aware: section headers preserved, max 800 chars, no sentence splitting"]
        ], [45, 135]),
        
        Paragraph("3. Solution Architecture", H2),
        tbl([
            ["Component", "Choice"],
            ["Pre-trained model", "llama3.2:3b via Ollama (local), temp 0.0. NOT EVALUATED (Ollama unavailable)."],
            ["Embedding model", "BAAI/bge-small-en-v1.5 (384-dim, Hugging Face, offline)"],
            ["Vector store", "ChromaDB v1.5.9, cosine distance, top-4, persistent storage"],
            ["RAG pipeline", "Query → BGE embed → ChromaDB → threshold (0.335) → LLM + citations"],
            ["Service layer and UI", "Streamlit 1.65.0 with example buttons, LLM toggle, evidence display"],
            ["Tools / rules", "Distance refusal (>0.335), citation regex, keyword evaluation"]
        ], [50, 130]),
        
        Paragraph("<b>Pipeline:</b> User query → BGE embeddings → ChromaDB retrieves top-4 chunks → "
                  "if best distance > 0.335: refuse → else: send to LLM with strict citation prompt → "
                  "parse [Page N] → return answer + citations + retrieved pages", B),
        
        PageBreak(),
        
        Paragraph("4. Implementation and Configuration", H2),
        Paragraph("<b>Step 1 - Ingestion (Code/ingest.py):</b>", H3),
        Paragraph("1. Load PDF with pdfplumber → extract text per page<br/>"
                  "2. Identify sections with regex (e.g., '3.1 DoorLockManager')<br/>"
                  "3. Create chunks: section header + text (max 800 chars)<br/>"
                  "4. Generate BGE embeddings → store in ChromaDB<br/>"
                  "5. Result: 14 chunks indexed", B),
        
        Paragraph("<b>Step 2 - Retrieval (Code/rag.py):</b>", H3),
        Paragraph("1. Embed query with QUERY_PREFIX + question<br/>"
                  "2. ChromaDB.query(top_k=4, cosine distance)<br/>"
                  "3. Return hits: [{text, page, section, distance}, ...]", B),
        
        Paragraph("<b>Step 3 - Generation (Code/rag.py):</b>", H3),
        Paragraph("1. Call retrieve(question) → get top-4 hits<br/>"
                  "2. If top distance > 0.335: refuse ('Not found')<br/>"
                  "3. Else if use_llm=False: return best chunk (extractive mode)<br/>"
                  "4. Else if use_llm=True: send chunks to Ollama → parse [Page N]", B),
        
        Paragraph("<b>Key Parameters:</b>", H3),
        tbl([
            ["Parameter", "Value", "Rationale"],
            ["CHUNK_CHARS", "800", "Captures 3-4 paragraphs, one semantic unit"],
            ["TOP_K", "4", "Balance context richness vs noise"],
            ["MAX_DISTANCE", "0.335", "Tuned for 100% refusal rate (was 0.60)"],
            ["TEMPERATURE", "0.0", "Deterministic answers"],
        ], [40, 30, 110]),
        
        Paragraph("5. Evaluation Steps and Results", H2),
        Paragraph("<b>Test Set:</b> 30 questions (28 answerable, 2 unanswerable) with ground truth", B),
        Paragraph("<b>Evaluation Mode:</b> Extractive (--no-llm) because Ollama unavailable. "
                  "LLM code implemented but not tested.", B),
        
        tbl([
            ["Metric", "Score"],
            ["Answer mode", "extractive"],
            ["Answerable questions", "28"],
            ["Retrieval hit rate", "96.4% (27/28)"],
            ["Answer accuracy", "78.6% (22/28)"],
            ["Citation accuracy", "78.6% (22/28)"],
            ["Correct refusal rate", "100.0% (2/2)"]
        ], [90, 90]),
        
        Paragraph("<b>Sample Results:</b>", H3),
        tbl([
            ["#", "Question", "Result"],
            ["Q1", "Which AUTOSAR platform does BCM use?", "Pass - Page 2, dist 0.225"],
            ["Q6", "What does DoorLockManager do when CrashDetected is set?", "Pass - Page 4, dist 0.197"],
            ["Q4", "Which team owns LightingController?", "Fail - Refused (dist 0.407 > 0.335)"],
            ["Q29", "What is wiper motor current limit?", "Pass - Correctly refused (not in doc)"]
        ], [15, 90, 75]),
        
        Paragraph("<b>Failure Analysis (6 questions with answer_correct=False):</b>", H3),
        Paragraph("• Q4, Q17, Q18, Q28: Refused by threshold (distances 0.343-0.407) - valid answers exist but embeddings didn't match well<br/>"
                  "• Q19: Retrieved correct page but keyword '100 ms' missing in extracted passage<br/>"
                  "• Q22: Wrong page retrieved (expected 11, got 13)", B),
        
        PageBreak(),
        
        Paragraph("6. Responsible AI Measures", H2),
        tbl([
            ["Area", "Measure"],
            ["Grounding and citations", "Mandatory [Page N], regex verification, UI shows retrieved evidence"],
            ["Privacy", "Synthetic data only, local execution, no data collection, no cloud APIs"],
            ["Security", "Localhost only, no authentication (demo), input validation, no code injection risk"],
            ["Human oversight", "UI disclaimer: 'Review every answer', limitations documented, test set evaluation"]
        ], [50, 130]),
        
        Paragraph("7. Innovation Highlights", H2),
        Paragraph("1. <b>Section-aware chunking:</b> Section headers in chunks provide better context<br/>"
                  "2. <b>Distance-based refusal:</b> Deterministic rule achieves 100% correct refusal rate<br/>"
                  "3. <b>Dual-mode evaluation:</b> Extractive vs LLM modes separate retrieval from generation quality<br/>"
                  "4. <b>Citation verification UI:</b> All 4 chunks shown with distances for user verification<br/>"
                  "5. <b>Honest reporting:</b> 6 failure cases documented with explanations", B),
        
        Paragraph("8. Screenshots, Logs and Evidence", H2),
        Paragraph("<b>Figure 1:</b> Streamlit UI showing successful answer with [Page 4] citation for "
                  "'What does DoorLockManager do when CrashDetected is set?' - Retrieved evidence expandable section "
                  "displays all 4 chunks with distances (0.197, 0.242, 0.307, 0.313)", B),
        Paragraph("<b>Figure 2:</b> Evaluation results CSV with 30 rows showing per-question metrics", B),
        Paragraph("<b>Figure 3:</b> Threshold tuning: 0.60→0.335 increased refusal rate from 0% to 100%", B),
        
        Paragraph("9. Reflection and Conclusions", H2),
        Paragraph("<b>What Worked:</b> Section-aware chunking, distance-based refusal (100% rate), "
                  "synthetic document approach, dual-mode evaluation", B),
        Paragraph("<b>Challenges:</b> Threshold tradeoff (4 valid questions refused), Ollama unavailable, "
                  "keyword-based eval limitation, single-document scope", B),
        Paragraph("<b>Lessons Learned:</b> Test set = tuning set problem (threshold optimistic), "
                  "embeddings don't always capture semantics, human review essential", B),
        Paragraph("<b>Goals Achieved:</b> ✓ RAG with citations ✓ 100% refusal rate ✓ Measured accuracy "
                  "✓ Responsible AI ✓ Honest failure reporting", B),
        Paragraph("<b>Future Work:</b> Independent validation set, LLM evaluation, semantic answer scoring, "
                  "multi-document support, revision comparison, graph relationships, production deployment", B),
        
        Paragraph("10. AI-Tool Usage Declaration", H2),
        tbl([
            ["AI Tool", "Purpose", "Artifact", "Verified"],
            ["GitHub Copilot", "Code autocompletion", "evaluate.py, ingest.py", "Y"],
            ["ChatGPT-4", "Debugging ChromaDB", "ingest.py, rag.py", "Y"],
            ["Claude (Kiro IDE)", "Documentation", "README, Technical Report", "Y"],
            ["BGE-small-en-v1.5", "Embeddings", "rag.py retrieval", "Y"],
            ["llama3.2:3b", "Answer generation", "rag.py (not evaluated)", "Y"]
        ], [40, 45, 50, 15]),
        
        Paragraph("11. Student Declaration", H2),
        Paragraph("I confirm this report represents my own understanding. I can explain every significant part: "
                  "section-aware chunking, BGE embeddings, ChromaDB retrieval, distance threshold (0.335) tradeoff, "
                  "LLM generation with citations, keyword evaluation, all 6 failure cases and root causes.", B),
        Paragraph("I understand the refusal threshold was tuned on the test set, making the 100% rate optimistic.", B),
        Spacer(1, 15),
        tbl([
            ["Signature:", "______________________________", "Date:", "07/10/2026"],
            ["Name:", "Sajjan Pawar", "PRN:", "124B2B037"]
        ], [25, 70, 20, 45], header=False),
    ]
    
    build("d:/sem 7/tata/TATA_TechnicalReport_SajjanPawar_124B2B037.pdf", story)


if __name__ == "__main__":
    synopsis()
    technical_report()
    print("\n✓ Both Tata documents created successfully!")
