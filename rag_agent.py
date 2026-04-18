import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# 1. API Configuration - Key successfully recovered
os.environ["OPENAI_API_KEY"] = "your key"

class RAGAgent:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.db_path = "./chroma_db"
        self.vector_db = None

    def ingest_document(self, pdf_path):
        """Reads, splits, and stores the PDF content into the vector database."""
        if not os.path.exists(pdf_path):
            print(f"Error: File not found at: {pdf_path}")
            return False

        print(f"\n--- 🧠 Processing document: {pdf_path} ---")
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(pages)

        self.vector_db = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings,
            persist_directory=self.db_path
        )
        print("--- ✅ Document indexed successfully! ---\n")
        return True

    def start_chat(self):
        """Starts an interactive Q&A session in the terminal."""
        if not self.vector_db:
            if os.path.exists(self.db_path):
                self.vector_db = Chroma(persist_directory=self.db_path, embedding_function=self.embeddings)
            else:
                print("Error: Vector database not found. You must ingest a PDF first.")
                return

        llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm, 
            chain_type="stuff", 
            retriever=self.vector_db.as_retriever(search_kwargs={"k": 3})
        )

        print("🤖 AI Expert Ready! Ask a question about your document (type 'exit' to quit):")
        while True:
            query = input("\nYou: ")
            if query.lower() in ["exit", "quit", "close"]:
                print("Goodbye!")
                break
            
            print("🔍 Thinking...")
            response = qa_chain.invoke(query)
            print(f"AI: {response['result']}")

if __name__ == "__main__":
    agent = RAGAgent()
    
    # Verificăm ce fișiere vede scriptul în folderul docs
    if os.path.exists("docs"):
        print(f"Files found in 'docs': {os.listdir('docs')}")
    else:
        print("Error: The 'docs' folder does not exist!")

    pdf_name = "document.pdf" 
    path = os.path.join("docs", pdf_name)

    # FORȚĂM citirea documentului
    # Asigură-te că NU ai # în față la linia de mai jos:
    success = agent.ingest_document(path)
    
    if success:
        agent.start_chat()
    else:
        print("Ingestion failed. Please check if 'document.pdf' is inside the 'docs' folder.")