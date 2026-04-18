import streamlit as st
import json
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import random
import os
import glob
from dotenv import load_dotenv

from yt_scrape.utils import clean_title, deduplicate_videos

# Load environment variables
load_dotenv()
# ... (rest of imports)

# Load all JSON data from the scraped_data directory
@st.cache_data
def load_all_scraped_data(directory="scraped_data"):
    import glob
    all_videos = []
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    if not json_files:
        return []
        
    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Check for both "videos" key or top-level list
                    all_videos.extend(data.get("videos", []))
                elif isinstance(data, list):
                    all_videos.extend(data)
        except Exception as e:
            st.warning(f"⚠️ Could not load {json_path}: {e}")
            
    # Deduplicate videos by ID
    unique_videos = deduplicate_videos(all_videos)
    return unique_videos

# Extract text from JSON data (legacy function for testing/internal use)
def extract_text_from_json(json_data):
    if isinstance(json_data, dict):
        videos = json_data.get("videos", [])
    else:
        videos = json_data
        
    texts = []
    for video in videos:
        raw_title = video.get("title", "")
        title = clean_title(raw_title)
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
    # Detect if we have a GPU
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available():
        device = "mps"
    
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

# Create FAISS vector store
def create_faiss_vector_store(texts, path="faiss_index"):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(texts, embedding=embeddings)
    vector_store.save_local(path)

# Load FAISS vector store
@st.cache_resource
def load_faiss_vector_store(path="faiss_index"):
    embeddings = get_embeddings()
    # allow_dangerous_deserialization is required for loading local FAISS indices in newer versions
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

# Show a random Bollywood quote/fact
st.markdown(
    f"<div style='text-align:center; color:#e91e63; font-size:22px; margin-bottom:10px;'>"
    f"💬 <i>{random.choice(BOLLYWOOD_QUOTES)}</i></div>",
    unsafe_allow_html=True
)

# Chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Reusable function to rebuild the index
def perform_rebuild(videos):
    if not videos:
        st.error("😅 Kya karen, no video data to index!")
        return False
        
    texts = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, video in enumerate(videos):
        if i % 500 == 0:
            progress = (i / len(videos))
            progress_bar.progress(progress)
            status_text.text(f"📝 Processing video {i}/{len(videos)}...")
            
        raw_title = video.get("title", "")
        title = clean_title(raw_title)
        description = str(video.get("description", ""))[:500]
        view_count = video.get("view_count", 0)
        like_count = video.get("like_count", 0)
        comment_count = video.get("comment_count", 0)
        published_at = video.get("published_at", "")
        channel = video.get("channel_name", "Unknown Channel")
        duration = video.get("duration", "N/A")

        text = (
            f"Title: {title}\n"
            f"Channel: {channel}\n"
            f"Duration: {duration}\n"
            f"Views: {view_count}\n"
            f"Likes: {like_count}\n"
            f"Comments: {comment_count}\n"
            f"Date: {published_at}\n"
            f"Description: {description}\n\n"
        )
        texts.append(text)

    status_text.text(f"✨ Indexing {len(texts)} videos... Don ko pakadna mushkil hi nahi, namumkin hai!")
    create_faiss_vector_store(texts)
    progress_bar.progress(1.0)
    status_text.text("✅ Knowledge base successfully rebuilt!")
    return True

# Check if rebuild is needed based on file timestamps
def check_rebuild_needed(directory="scraped_data", index_path="faiss_index"):
    if not os.path.exists(index_path):
        return True, "Index missing"
        
    import glob
    json_files = glob.glob(os.path.join(directory, "*.json"))
    if not json_files:
        return False, "No data files"
        
    # Get latest modification time of any JSON file
    latest_data_time = max(os.path.getmtime(f) for f in json_files)
    
    # Get modification time of the index
    index_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(index_file):
        return True, "Index file missing"
        
    index_time = os.path.getmtime(index_file)
    
    if latest_data_time > index_time:
        return True, "New data detected"
        
    return False, "Up to date"

# Load and process data from folder
try:
    rebuild_required, reason = check_rebuild_needed()
    
    # Sidebar for management
    with st.sidebar:
        st.header("⚙️ Data Management")
        st.write(f"Status: **{reason}**")
        
        if rebuild_required:
            st.warning("⚠️ Your knowledge base is out of date!")
            if st.button("🚀 Update Knowledge Base Now", type="primary"):
                import shutil
                if os.path.exists("faiss_index"):
                    shutil.rmtree("faiss_index")
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()
        else:
            if st.button("🔄 Force Rebuild Index"):
                import shutil
                if os.path.exists("faiss_index"):
                    shutil.rmtree("faiss_index")
                st.cache_data.clear()
                st.cache_resource.clear()
                st.rerun()

    # Rebuild if index missing or explicitly requested
    if not os.path.exists("faiss_index"):
        st.info(f"🎭 {reason}... Rebuilding the Bollywood Hungama knowledge base!")
        videos = load_all_scraped_data()
        if perform_rebuild(videos):
            st.rerun()
            
except Exception as e:
    st.error(f"😱 Arre baba! Error in data management: {e}")
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
    docs = retriever.invoke(retrieval_query)
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
