import streamlit as st
import os
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain

# --- 1. API CONFIGURATION ---
os.environ["OPENAI_API_KEY"] = "your-key"

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Ultimate AI Researcher", page_icon="🚀", layout="wide")

# --- 3. UI CUSTOMIZATION (SIDEBAR DROPDOWN) ---
if "ui_colors" not in st.session_state:
    st.session_state.ui_colors = {
        "Page Background": "#0E1117",
        "Sidebar Color": "#1A1C24",
        "Text Color": "#FFFFFF",
        "Accent Color (Buttons)": "#FF4B4B"
    }

with st.sidebar:
    st.title("🎨 UI Settings")
    
    # Dropdown pentru selectarea elementului
    target_element = st.selectbox(
        "Ce vrei să personalizezi?",
        list(st.session_state.ui_colors.keys())
    )
    
    # Color Picker care modifică valoarea în session_state
    new_color = st.color_picker(f"Alege culoarea pentru {target_element}", st.session_state.ui_colors[target_element])
    st.session_state.ui_colors[target_element] = new_color

    st.divider()
    st.header("📁 Document Management")
    uploaded_files = st.file_uploader("Upload PDFs", accept_multiple_files=True, type=['pdf'])

# Extragem culorile pentru CSS
colors = st.session_state.ui_colors

# Inject Dynamic CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {colors["Page Background"]};
        color: {colors["Text Color"]};
    }}
    [data-testid="stSidebar"] {{
        background-color: {colors["Sidebar Color"]} !important;
    }}
    .stButton>button {{
        background-color: {colors["Accent Color (Buttons)"]} !important;
        color: white !important;
        border-radius: 10px;
        border: none;
        width: 100%;
    }}
    p, h1, h2, h3, span, label, .stMarkdown {{
        color: {colors["Text Color"]} !important;
    }}
    .stChatMessage {{
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        margin-bottom: 10px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. RAG LOGIC ---
if not os.path.exists("docs"): os.makedirs("docs")

def get_vector_db():
    if "vector_db" not in st.session_state:
        if os.path.exists("./chroma_db"):
            st.session_state.vector_db = Chroma(
                persist_directory="./chroma_db", 
                embedding_function=OpenAIEmbeddings()
            )
        else:
            st.session_state.vector_db = None
    return st.session_state.vector_db

def process_docs():
    with st.spinner("🚀 Indexing your knowledge base..."):
        loader = DirectoryLoader("docs/", glob="./*.pdf", loader_cls=PyPDFLoader)
        docs = loader.load()
        if not docs:
            st.error("No PDF files found in 'docs' folder!")
            return
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=OpenAIEmbeddings(),
            persist_directory="./chroma_db"
        )
        st.session_state.vector_db = vector_db
        st.success(f"Indexed {len(docs)} documents successfully!")

# --- 5. SIDEBAR ACTIONS ---
with st.sidebar:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔥 Rebuild"):
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    with open(os.path.join("docs", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                process_docs()
            else: st.warning("Upload files first!")
    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()

# --- 6. MAIN CHAT INTERFACE ---
st.title("🤖 Ultimate AI Researcher")

if "messages" not in st.session_state: st.session_state.messages = []
if "chat_history" not in st.session_state: st.session_state.chat_history = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    db = get_vector_db()
    if not db:
        st.error("Database is empty. Please upload PDFs and click 'Rebuild'.")
    else:
        with st.chat_message("assistant"):
            llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
            chain = ConversationalRetrievalChain.from_llm(
                llm=llm,
                retriever=db.as_retriever(search_kwargs={"k": 3}),
                return_source_documents=True
            )
            with st.spinner("Searching..."):
                result = chain.invoke({"question": prompt, "chat_history": st.session_state.chat_history})
                answer = result["answer"]
                st.markdown(answer)
                with st.expander("📌 View Document Sources"):
                    for i, doc in enumerate(result["source_documents"]):
                        source_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
                        page = doc.metadata.get('page', 'N/A')
                        st.write(f"**{i+1}:** {source_name} (Page {page})")
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.chat_history.append((prompt, answer))