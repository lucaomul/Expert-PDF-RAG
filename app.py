import streamlit as st
import os
import tempfile
import chromadb

# --- IMPORTURI CORE ---
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

# --- FIX PENTRU EROAREA DE IMPORT (LINIA 13-15) ---
# Importăm din rutele noi, specifice versiunii 0.3
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# --- CONFIGURARE PAGINĂ ---
st.set_page_config(
    page_title="ChatPDF | Terminal v5.2",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- FULL MIA UI DESIGN (CSS) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

.stApp { 
    background-color: #0a0a0f !important; 
    color: #e2e2e2; 
    font-family: 'IBM Plex Sans', sans-serif; 
}

[data-testid="stSidebar"] { 
    background-color: #0d0d16 !important; 
    border-right: 1px solid #1a1a2e; 
    min-width: 320px !important; 
}

.sidebar-title { 
    font-family: 'IBM Plex Mono', monospace; 
    font-size: 1.3rem; 
    font-weight: 600; 
    color: #00ff88; 
    letter-spacing: 0.2em; 
    margin-bottom: 0.2rem; 
}

.sidebar-subtitle { 
    font-family: 'IBM Plex Mono', monospace; 
    font-size: 0.7rem; 
    color: #555577; 
    margin-bottom: 2rem; 
    text-transform: uppercase; 
}

.section-label { 
    font-family: 'IBM Plex Mono', monospace; 
    font-size: 0.75rem; 
    color: #ffffff !important; 
    text-transform: uppercase; 
    margin-top: 1.5rem; 
    border-left: 3px solid #00ff88; 
    padding-left: 10px; 
    margin-bottom: 12px; 
    font-weight: 600; 
}

.stButton > button { 
    background: #00ff88 !important; 
    color: #0a0a0f !important; 
    font-family: 'IBM Plex Mono', monospace !important; 
    font-weight: 700 !important; 
    border: none !important; 
    width: 100%; 
    padding: 0.6rem;
    transition: 0.3s;
}

.stButton > button:hover { 
    transform: translateY(-2px); 
    box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3); 
}

.chat-card-ai { 
    background: #11111d; 
    border: 1px solid #1a1a2e; 
    padding: 20px; 
    border-radius: 8px; 
    margin-top: 15px; 
    border-left: 4px solid #00ff88; 
    box-shadow: 5px 5px 15px rgba(0,0,0,0.3); 
}

.chat-card-user { 
    background: #161625; 
    border: 1px solid #1a1a2e; 
    padding: 15px; 
    border-radius: 8px; 
    margin-top: 10px; 
    border-left: 4px solid #ffffff33; 
}

.source-tag {
    background: #1a1a2e;
    color: #00ff88;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-family: 'IBM Plex Mono', monospace;
    border: 1px solid #00ff8833;
    margin-right: 8px;
    margin-top: 8px;
    display: inline-block;
}

.sidebar-footer { 
    margin-top: 4rem; 
    padding-top: 1.5rem; 
    border-top: 1px solid #1a1a2e; 
}

.empowered-text { 
    font-size: 0.75rem; 
    color: #8888aa; 
    margin-bottom: 10px; 
    font-family: 'IBM Plex Mono', monospace; 
    font-weight: 600; 
}

.social-link { 
    display: block; 
    font-size: 0.75rem; 
    color: #00ff88; 
    text-decoration: none; 
    margin-bottom: 6px; 
    font-family: 'IBM Plex Mono', monospace; 
}
</style>
""", unsafe_allow_html=True)

# --- INIT ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">⬡ ChatPDF</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Modern Stack v5.2</div>', unsafe_allow_html=True)
    
    api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("INITIALIZE ENGINE"):
        if not api_key or not uploaded_files:
            st.error("Credentials Required")
        else:
            os.environ["OPENAI_API_KEY"] = api_key
            with st.status("🚀 Overclocking Neural Engine...", expanded=True) as status:
                all_splits = []
                for f in uploaded_files:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                        tmp.write(f.getvalue())
                        tmp_path = tmp.name
                    loader = PyPDFLoader(tmp_path)
                    docs = loader.load()
                    for d in docs: d.metadata["source_file"] = f.name
                    all_splits.extend(RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs))
                    os.remove(tmp_path)
                
                client = chromadb.EphemeralClient()
                vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), client=client)
                llm = ChatOpenAI(model="gpt-4o", temperature=0)
                
                # Chain Construction
                h_retriever = create_history_aware_retriever(llm, vectorstore.as_retriever(), ChatPromptTemplate.from_messages([
                    ("system", "Standalone query rewriter."), MessagesPlaceholder("chat_history"), ("human", "{input}")
                ]))
                qa_chain = create_stuff_documents_chain(llm, ChatPromptTemplate.from_messages([
                    ("system", "Context-based answerer:\n\n{context}"), MessagesPlaceholder("chat_history"), ("human", "{input}")
                ]))
                st.session_state.rag_chain = create_retrieval_chain(h_retriever, qa_chain)
                status.update(label="System Calibrated.", state="complete")
                st.rerun()

    if st.button("PURGE MEMORY"):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown(f"""
    <div class="sidebar-footer">
        <div class="empowered-text">Empowered by Luca Crăciun</div>
        <a href="https://github.com/lucaomul" target="_blank" class="social-link">GITHUB_REPO</a>
        <a href="https://www.linkedin.com/in/gabriel-luca-craciun-25ba95295" target="_blank" class="social-link">LINKEDIN_NODE</a>
    </div>
    """, unsafe_allow_html=True)

# --- CHAT ---
st.markdown('<h2 style="color:#00ff88; font-family:IBM Plex Mono;">TERMINAL_PROMPT ></h2>', unsafe_allow_html=True)

if st.session_state.rag_chain:
    for m in st.session_state.chat_history:
        role = "chat-card-user" if isinstance(m, HumanMessage) else "chat-card-ai"
        st.markdown(f'<div class="{role}">{m.content}</div>', unsafe_allow_html=True)

    query = st.text_input("Query:", key="main_input")
    if query:
        res = st.session_state.rag_chain.invoke({"input": query, "chat_history": st.session_state.chat_history})
        st.session_state.chat_history.append(HumanMessage(content=query))
        st.session_state.chat_history.append(AIMessage(content=res["answer"]))
        
        st.markdown("<div style='font-size:0.7rem; color:#555; margin-top:10px;'>SOURCES:</div>", unsafe_allow_html=True)
        sources = sorted(list(set([f"{d.metadata.get('source_file')} [Pg. {d.metadata.get('page',0)+1}]" for d in res["context"]])))
        for s in sources: st.markdown(f'<div class="source-tag">📄 {s}</div>', unsafe_allow_html=True)
        st.rerun()
else:
    st.info("System Standby. Please initialize via sidebar.")