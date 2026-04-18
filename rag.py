import streamlit as st
import json
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import random
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Groq
API_KEY = os.getenv('GROQ_API_KEY', 'SET YOUR OWN API KEY')
client = Groq(api_key=API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# Load JSON data from a file
def load_json_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Extract text from JSON data
def extract_text_from_json(json_data):
    texts = []
    for video in json_data.get("videos", []):
        title = video.get("title", "")
        description = video.get("description", "")
        view_count = video.get("view_count", 0)
        like_count = video.get("like_count", 0)
        comment_count = video.get("comment_count", 0)
        published_at = video.get("published_at", "")

        text = f"Title: {title}\nDescription: {description}\nViews: {view_count}\nLikes: {like_count}\n Comments: {comment_count}\n Date: {published_at}\n\n"
        texts.append(text)
    return texts

# Cache the embeddings model
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create FAISS vector store
def create_faiss_vector_store(texts, path="faiss_index"):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(texts, embedding=embeddings)
    vector_store.save_local(path)

# Load FAISS vector store
@st.cache_resource
def load_faiss_vector_store(path="faiss_index"):
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# Bollywood quotes/facts
BOLLYWOOD_QUOTES = [
    "“Bade bade deshon mein aisi choti choti baatein hoti rehti hain!” 🎬",
    "“Mogambo khush hua!” 😎",
    "“Picture abhi baaki hai mere dost!” 🍿",
    "“Don ko pakadna mushkil hi nahi, namumkin hai!” 🕶️",
    "“All is well!” 🤞",
    "“How’s the josh? High Sir!” 💥",
]

# Funky Bollywood loading quotes
BOLLYWOOD_LOADING_QUOTES = [
    "🎬 Loading... Picture abhi baaki hai mere dost!",
    "💃🕺 Loading... How’s the josh? High Sir!",
    "🍿 Loading... Mogambo khush hua!",
    "🎤 Loading... All is well!",
    "🕶️ Loading... Don ko pakadna mushkil hi nahi, namumkin hai!",
    "✨ Loading... Bade bade deshon mein aisi choti choti baatein hoti rehti hain!",
]

# Streamlit App
st.markdown(
    """
    <div style='text-align: center;'>
        <img src='https://www.bollywoodhungama.com/wp-content/themes/bh-theme/images/logo.png' width='250'/>
        <h1 style='color: #e50914; font-family: "Comic Sans MS", cursive, sans-serif;'>Bollywood Hungama Chatbot 🎬✨</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Show a random Bollywood quote/fact (not loading quote)
st.markdown(
    f"<div style='text-align:center; color:#e91e63; font-size:22px; margin-bottom:10px;'>"
    f"💬 <i>{random.choice(BOLLYWOOD_QUOTES)}</i></div>",
    unsafe_allow_html=True
)

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

JSON_PATH = "youtube_videos.json"

# Load and process JSON data
try:
    if not os.path.exists("faiss_index"):
        st.info(random.choice(BOLLYWOOD_LOADING_QUOTES))
        json_data = load_json_data(JSON_PATH)
        texts = extract_text_from_json(json_data)
        if not texts:
            st.error("😅 Kya karen, no usable content found in the JSON file!")
            st.stop()
        create_faiss_vector_store(texts)
except Exception as e:
    st.error(f"😱 Arre baba! Error loading/processing data: {e}")
    st.stop()

st.info("🎬 Lights, Camera, Action! The chatbot is ready for your Bollywood questions!")
vector_store = load_faiss_vector_store()

question = st.text_input("🎤 Ask a question about YouTube videos:")

# Give your Bollywood bot a fun name!
BOT_NAME = "HungamaBot"

if question:
    # Build chat history string for retrieval (limit to last 3 for context)
    retrieval_query = ""
    for entry in st.session_state.chat_history[-3:]:
        retrieval_query += f"User: {entry['question']}\n{BOT_NAME}: {entry['answer']}\n"
    retrieval_query += f"User: {question}"

    st.info("🔎 Searching for your answer... Don ko pakadna mushkil hi nahi, namumkin hai!")
    retriever = vector_store.as_retriever()
    docs = retriever.get_relevant_documents(retrieval_query)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Build chat history string for bot prompt (limit to last 5 for bot)
    history_str = ""
    for entry in st.session_state.chat_history[-5:]:
        history_str += f"User: {entry['question']}\n{BOT_NAME}: {entry['answer']}\n"

    # Compose prompt with history
    prompt = (
        f"{history_str}"
        f"Context:\n{context}\n\n"
        f"User: {question}\n{BOT_NAME}:"
    )

    st.info(f"🤖 {BOT_NAME} is thinking... Picture abhi baaki hai mere dost!")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"You are {BOT_NAME}, a fun Bollywood-themed bot. Answer questions using the provided context."
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL_NAME,
    )
    answer = chat_completion.choices[0].message.content if chat_completion.choices else "No response from HungamaBot."
    st.session_state.chat_history.append({"question": question, "answer": answer})
    st.success("🎉 Mogambo khush hua! Here's your Bollywood answer!")

# Display chat history with Bollywood style
if st.session_state.chat_history:
    st.markdown("### 📝 Chat History")
    for entry in st.session_state.chat_history[::-1]:
        st.markdown(
            f"<div style='background:#f3f7fa; border-radius:10px; padding:10px; margin-bottom:8px;'>"
            f"<b style='color:#1976d2;'>🧑‍🎤 You:</b> <span style='color:#333;'>{entry['question']}</span><br>"
            f"<b style='color:#388e3c;'>🤖 {BOT_NAME}:</b> <span style='color:#222;'>{entry['answer']}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

# Funky Bollywood footer
st.markdown(
    """
    <hr>
    <div style='text-align:center; font-size:16px; color:#ff9800;'>
        Made with ❤️ for Bollywood fans | <a href='https://www.instagram.com/zeemusiccompany/' target='_blank'>Follow Zee Music on Instagram</a>
    </div>
    """,
    unsafe_allow_html=True
)
