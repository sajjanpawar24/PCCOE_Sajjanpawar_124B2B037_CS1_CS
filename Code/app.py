"""Streamlit demo.  Run:  streamlit run Code/app.py"""
import streamlit as st

import config
import ingest
import rag

st.set_page_config(page_title="AUTOSAR HLD Assistant", layout="wide")
st.title("AUTOSAR HLD Document Analysis Assistant")
st.caption("Ask questions about the synthetic BCM High-Level Design. Answers use only the document and show page citations.")

with st.sidebar:
    st.subheader("Knowledge base")
    st.write(f"Document: `{config.PDF_PATH.name}`")
    st.write(f"Embeddings: `{config.EMBED_MODEL}`")
    st.write(f"LLM: `{config.OLLAMA_MODEL}` (local, Ollama)")
    use_llm = st.checkbox("Use LLM (off = show best passage only)", value=True)
    if st.button("Rebuild index"):
        with st.spinner("Indexing..."):
            n = ingest.build_index()
            rag._resources.cache_clear()
        st.success(f"Indexed {n} chunks")
    st.info("Review every answer against the cited page before using it. The assistant supports engineers; it does not approve designs.")

examples = ["What does DoorLockManager do when CrashDetected is set?", "What are the lux thresholds for automatic headlights?",
            "Which interface type is Pp_BcmMode?", "What is the current limit of the wiper motor?"]
cols = st.columns(len(examples))
for c, ex in zip(cols, examples):
    if c.button(ex):
        st.session_state["q"] = ex

q = st.text_input("Your question", key="q")
if q:
    with st.spinner("Searching and answering..."):
        res = rag.answer(q, use_llm=use_llm)
    st.subheader("Answer")
    st.write(res["answer"])
    st.caption(f"Mode: {res['mode']} | Cited pages: {res['cited']} | Best-match distance: {res['top_distance']}")
    if "llm_error" in res:
        st.warning("LLM not reachable, showing the best passage instead. Start Ollama to get full answers.")
    with st.expander("Retrieved evidence"):
        for h in res["hits"]:
            st.markdown(f"**Page {h['page']}**, {h['section']} (distance {h['distance']:.3f})")
            st.text(h["text"])
