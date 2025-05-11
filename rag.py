import streamlit as st
import os
import zipfile
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai


# Configure Gemini
genai.configure(api_key="AIzaSyCWWp87jq69qbFdC2hIvd1B7QgZf0QuS5U")
model = genai.GenerativeModel("gemini-1.5-pro")

# Extract text from SQL file 
def extract_text_from_sql(sql_path):
    with open(sql_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

# Extract SQL files from zip and return their combined content
def extract_sql_from_zip(zip_path, extract_to="unzipped_sqls"):
    os.makedirs(extract_to, exist_ok=True)
    text = ""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        for root, _, files in os.walk(extract_to):
            for file in files:
                if file.endswith(".sql"):
                    file_path = os.path.join(root, file)
                    text += extract_text_from_sql(file_path) + "\n"
    return text

# Create FAISS vector store
def create_faiss_vector_store(text, path="faiss_index"):
    # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    # chunks = splitter.split_text(text)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts([text], embedding=embeddings)
    vector_store.save_local(path)

# Load FAISS vector store
def load_faiss_vector_store(path="faiss_index"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# Streamlit App
st.title("RAG Chatbot with SQL Files")
st.write("Upload a .SQL file or a .ZIP containing SQL files. Ask questions based on the contents.")

uploaded_file = st.file_uploader("Upload your .SQL or .ZIP file", type=["sql", "zip"])

if uploaded_file is not None:
    os.makedirs("uploaded", exist_ok=True)
    file_path = f"uploaded/{uploaded_file.name}"
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Determine file type and extract text
    if uploaded_file.name.endswith(".sql"):
        text = extract_text_from_sql(file_path)
    elif uploaded_file.name.endswith(".zip"):
        st.info("Extracting SQL files from ZIP...")
        text = extract_sql_from_zip(file_path)
    else:
        st.error("Unsupported file type.")
        st.stop()

    if not text.strip():
        st.error("No usable SQL content found.")
        st.stop()

    st.info("Creating FAISS vector store...")
    create_faiss_vector_store(text)
    st.info("Vector store created.")
    st.success("Chatbot is ready!")
    vector_store = load_faiss_vector_store()

    question = st.text_input("Ask a question about the SQL content:")
    if question:
        st.info("Retrieving context from the content...")
        retriever = vector_store.as_retriever()
        docs = retriever.get_relevant_documents(question)
        context = "\n\n".join([doc.page_content for doc in docs])

        prompt = f"""Answer the question based on the following context:\n\n{context}\n\nQuestion: {question}"""
        st.info("Querying Gemini...")
        response = model.generate_content(prompt)
        answer = response.text if response else "No response from Gemini."
        st.markdown(f"**Answer:** {answer}")
