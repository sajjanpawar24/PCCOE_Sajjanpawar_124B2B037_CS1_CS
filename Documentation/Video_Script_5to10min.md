# Demo video script (target 7 minutes). Record screen + voice.

1. (0:00-0:40) Intro: your name, project title, problem: HLD documents are long, searching is slow.
2. (0:40-1:40) Knowledge base: open Input_Data/BCM_HLD_v1.0.pdf, scroll 3-4 pages (component table, ports, CAN signals). Say it is synthetic.
3. (1:40-3:00) Pipeline: show Code/ingest.py and rag.py. Say: pdfplumber -> chunks per section -> BGE embeddings -> ChromaDB -> top-4 -> local llama3.2:3b -> answer with [Page N]. Show Model_Prompts_Config/system_prompt.txt.
4. (3:00-5:00) Live demo in Streamlit (streamlit run Code/app.py). Ask 4 questions:
   - What happens when CrashDetected is set?  (expect: unlock all doors within 100 ms, page 4)
   - What are the lux thresholds for automatic headlights?  (400 / 800, page 6 or 11)
   - Which interface type is Pp_BcmMode?  (Mode-Switch, page 8)
   - What is the current limit of the wiper motor?  (expect: Not found in the document)
   Open "Retrieved evidence" once to show the cited page text.
5. (5:00-6:30) Evaluation: show Evaluation_Results/summary.json and results.csv. Read the 4 metrics. Show one wrong answer honestly and say why.
6. (6:30-7:30) Limitations and future work, then thank you.
Tip: run one test question before recording so the model is already loaded.
