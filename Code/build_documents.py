"""Builds the printable PDFs: Synopsis, Declaration, Technical Report.
Edit Documentation/student_info.json first. Run after evaluate.py so the report has real numbers.
Run:  python Code/build_documents.py
"""
import csv
import json

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import config

ROOT = config.ROOT
INFO = json.loads((ROOT / "Documentation" / "student_info.json").read_text(encoding="utf-8"))
ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=15, spaceBefore=6, spaceAfter=6)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12, spaceBefore=8, spaceAfter=4)
B = ParagraphStyle("B", parent=ss["Normal"], fontSize=10.5, leading=15, spaceAfter=5)
C = ParagraphStyle("C", parent=ss["Normal"], fontSize=8.5, leading=10.5)
CH = ParagraphStyle("CH", parent=C, textColor=colors.white, fontName="Helvetica-Bold")
TITLE = ParagraphStyle("T", parent=ss["Title"], fontSize=20, leading=26)


def tbl(rows, widths, header=True):
    data = [[Paragraph(str(c), CH if (header and i == 0) else C) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F3A5F")))
    t.setStyle(TableStyle(st))
    return t


def build(path, story):
    path.parent.mkdir(parents=True, exist_ok=True)
    SimpleDocTemplate(str(path), pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm,
                      topMargin=18 * mm, bottomMargin=18 * mm).build(story)
    print("Wrote", path)


def who():
    return f"{INFO['student_name']} (PRN {INFO['prn']}, {INFO['division']})"


def synopsis():
    s = [Paragraph("Project Synopsis", TITLE), Paragraph(INFO["project_title"], H1),
         tbl([["Student", who()], ["Faculty guide", INFO["faculty_guide"]], ["Date", INFO["date"]],
              ["Course", "Applied AI/ML Project (Final Year, Computer Engineering, PCCOE)"]], [40, 130], header=False),
         Paragraph("1. Problem statement", H2),
         Paragraph("AUTOSAR High-Level Design (HLD) documents are long, unstructured PDFs. Engineers lose time searching "
                   "for component, interface, signal and dependency details, and wrong readings cause design mistakes.", B),
         Paragraph("2. Objectives", H2),
         Paragraph("- Build a Retrieval-Augmented Generation (RAG) assistant that answers questions about an HLD document.<br/>"
                   "- Every answer must carry a page citation, and the system must say 'Not found' when the document has no answer.<br/>"
                   "- Measure retrieval, answer and citation accuracy on a ground-truth question set.", B),
         Paragraph("3. Approach", H2),
         Paragraph("PDF text extraction (pdfplumber), section-wise chunking, BGE-small embeddings, ChromaDB vector store, "
                   "top-4 retrieval, local LLM (llama3.2:3b via Ollama) with a strict citation prompt, Streamlit interface. "
                   "Data is a synthetic 14-page Body Control Module HLD created for this project (no real company data).", B),
         Paragraph("4. Expected outcome", H2),
         Paragraph("A working assistant, a 30-question evaluation (28 answerable, 2 unanswerable), a technical report and a demo video.", B),
         Spacer(1, 10), Paragraph("Faculty approval record", H2),
         tbl([["Decision", "Remarks", "Faculty name", "Signature", "Date"],
              ["Approved / Changes needed", "", INFO["faculty_guide"], "", ""]], [38, 45, 35, 32, 20]),
         Spacer(1, 30), Paragraph(f"Student signature: ______________________   ({INFO['student_name']})", B)]
    build(ROOT / "Synopsis" / "Project_Synopsis.pdf", s)


def declaration():
    s = [Paragraph("Student Declaration", TITLE), Spacer(1, 12),
         Paragraph(f"I, <b>{INFO['student_name']}</b> (PRN {INFO['prn']}, {INFO['division']}), declare that the project "
                   f"'<b>{INFO['project_title']}</b>' is my own work. The input data is synthetic and contains no real, "
                   "confidential or copyrighted company or standards content. Any tool, library or model I used is declared "
                   "in the technical report. I understand that I must be able to explain my code, design choices, "
                   "evaluation results and limitations.", B),
         Spacer(1, 40), Paragraph("Signature: ______________________", B),
         Paragraph(f"Name: {INFO['student_name']}", B), Paragraph(f"Date: {INFO['date']}", B)]
    build(ROOT / "Declarations" / "Student_Declaration.pdf", s)


def report():
    sp, rp = config.RESULTS_DIR / "summary.json", config.RESULTS_DIR / "results.csv"
    have = sp.exists() and rp.exists()
    s = [Paragraph("Technical Report", TITLE), Paragraph(INFO["project_title"], H1),
         tbl([["Student", who()], ["Faculty guide", INFO["faculty_guide"]], ["Date", INFO["date"]]], [40, 130], header=False),
         Paragraph("1. Abstract", H2),
         Paragraph("This project builds a RAG assistant for AUTOSAR High-Level Design documents. It answers engineer questions "
                   "using only retrieved pages, cites the page for each answer, and refuses when the document has no answer. "
                   "It is evaluated on a ground-truth question set.", B),
         Paragraph("2. Problem and objectives", H2),
         Paragraph("HLD documents are long and unstructured, so finding a port, signal or dependency is slow and error-prone. "
                   "Objectives: (a) searchable question answering over an HLD, (b) page citations on every answer, "
                   "(c) safe refusal when the answer is missing, (d) measured accuracy.", B),
         Paragraph("3. Knowledge base", H2),
         Paragraph("A synthetic 14-page Body Control Module (BCM) HLD (Input_Data/BCM_HLD_v1.0.pdf) generated by "
                   "Code/generate_hld.py. It covers components, ports, CAN signals, functional flows, BSW dependencies, "
                   "diagnostics and revision history, with text and tables. No real or confidential data is used.", B),
         Paragraph("4. System design", H2),
         Paragraph("PDF -> pdfplumber text per page -> section chunks (max 800 characters, section title kept) -> "
                   "BAAI/bge-small-en-v1.5 embeddings -> ChromaDB (cosine) -> top-4 retrieval -> llama3.2:3b (Ollama, "
                   "temperature 0) with a strict prompt -> answer with [Page N] citations -> Streamlit UI.", B),
         tbl([["Item", "Value"], ["LLM", f"{config.OLLAMA_MODEL} via Ollama (local)"], ["Embeddings", config.EMBED_MODEL],
              ["Vector store", "ChromaDB, persistent, cosine distance"], ["Top-k", str(config.TOP_K)],
              ["Refusal threshold", f"best-match distance above {config.MAX_DISTANCE} gives 'Not found'"],
              ["Prompt", "Model_Prompts_Config/system_prompt.txt"], ["UI", "Streamlit"]], [45, 125]),
         Paragraph("5. Evaluation method", H2),
         Paragraph("30 questions with known answers and pages (Input_Data/test_questions.json): 28 answerable, 2 not in the "
                   "document. Metrics: retrieval hit rate (expected page among retrieved pages), answer accuracy (all required "
                   "keywords present), citation accuracy (expected page cited), and correct refusal rate on unanswerable questions. "
                   "The evaluation was run in extractive mode (retrieval + best passage extraction) because Ollama was not available. "
                   "The LLM generation step is implemented in rag.py but was not evaluated.", B),
         Paragraph("6. Results", H2)]
    if have:
        sm = json.loads(sp.read_text(encoding="utf-8"))
        s.append(tbl([["Metric", "Value"],
                      ["Answer mode used", sm["mode"]],
                      ["Answerable questions", sm["answerable_questions"]],
                      ["Retrieval hit rate", f"{sm['retrieval_hit_rate_pct']} %"],
                      ["Answer accuracy", f"{sm['answer_accuracy_pct']} %"],
                      ["Citation accuracy", f"{sm['citation_accuracy_pct']} %"],
                      ["Correct refusal rate (unanswerable)", f"{sm['correct_refusal_pct']} %"]], [90, 80]))
        rows = list(csv.DictReader(open(rp, encoding="utf-8")))
        fails = [r for r in rows if r["answer_correct"] != "True"]
        s.append(Paragraph("Questions answered incorrectly (from results.csv):", H2))
        if fails:
            s.append(tbl([["Q", "Question", "System answer (short)"]] +
                         [[r["id"], r["question"], r["answer"][:140]] for r in fails], [10, 70, 90]))
        else:
            s.append(Paragraph("None. All questions were answered or refused correctly.", B))
        s.append(Paragraph("Full per-question results are in Evaluation_Results/results.csv and sample outputs with citations "
                           "are in Evaluation_Results/sample_outputs.md.", B))
    else:
        s.append(Paragraph("<b>[RESULTS MISSING: run python Code/evaluate.py and then python Code/build_documents.py again]</b>", B))
    s += [Paragraph("7. Limitations", H2),
          Paragraph("- One synthetic document of 14 pages; text and simple tables only, no diagrams and no OCR.<br/>"
                    "- A small local model can miss multi-part answers or cite the wrong page.<br/>"
                    "- The refusal threshold is set by hand and may block valid questions or allow weak matches.<br/>"
                    "- The refusal threshold (0.335) was tuned on the same 30 evaluation questions, so the refusal rate is optimistic.<br/>"
                    "- Keyword-based answer checking can mark a correct paraphrase as wrong.<br/>"
                    "- The system assists engineers; every answer must be checked against the cited page.", B),
          Paragraph("8. External dependencies declared", H2),
          Paragraph("Internet is needed once to download the embedding model (Hugging Face) and the LLM (Ollama). "
                    "At run time everything works locally. No cloud API is used.", B),
          Paragraph("9. Future work", H2),
          Paragraph("Revision comparison, inconsistency checks, graph relationships between components, role-based access, "
                    "OCR for scanned pages, and a FastAPI service layer.", B),
          Paragraph("10. Contribution", H2),
          Paragraph(f"{INFO['student_name']}: designed the HLD document and ground-truth set, implemented ingestion, retrieval, "
                    "prompting, evaluation and the Streamlit interface, and wrote this report.", B),
          Paragraph("11. References", H2),
          Paragraph("AUTOSAR Classic Platform concepts (public documentation); BAAI BGE embeddings; ChromaDB; Ollama; "
                    "Streamlit; pdfplumber.", B)]
    build(ROOT / "Documentation" / "Technical_Report.pdf", s)


if __name__ == "__main__":
    synopsis()
    declaration()
    report()
