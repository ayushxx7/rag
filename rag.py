import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
import random
import os
import glob
import re
from datetime import datetime
from dotenv import load_dotenv

from yt_scrape.utils import clean_title, deduplicate_videos

# Set page config for a wider dashboard look
st.set_page_config(page_title="Bollywood Magic Dashboard", layout="wide", page_icon="🎬")

# Load environment variables
load_dotenv()

# Configure Groq
API_KEY = os.getenv('GROQ_API_KEY', 'SET YOUR OWN API KEY')
client = Groq(api_key=API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# Helper to extract artist/singer/movie from description
def extract_metadata(text, title):
    metadata = {"singers": [], "movie": "Unknown", "tags": []}
    
    # Extract Singers
    singer_match = re.search(r"Singer[s]?:\s*([^\n|]+)", text, re.IGNORECASE)
    if singer_match:
        metadata["singers"] = [s.strip() for s in re.split(r",|&", singer_match.group(1))]
    
    # Extract Movie
    movie_match = re.search(r"Movie:\s*([^\n|]+)", text, re.IGNORECASE)
    if movie_match:
        metadata["movie"] = movie_match.group(1).strip()
        
    # Smart Tagging
    if any(k in (text + title).lower() for k in ["rap", "hip hop", "honey singh", "badshah", "raftaar"]):
        metadata["tags"].append("Rap/Hip-Hop")
    if any(k in (text + title).lower() for k in ["sad", "dard", "judai", "broken"]):
        metadata["tags"].append("Emotional/Sad")
    if any(k in (text + title).lower() for k in ["party", "dance", "club", "nachta"]):
        metadata["tags"].append("Party/Dance")
    if any(k in (text + title).lower() for k in ["bhakti", "bhajan", "devotional"]):
        metadata["tags"].append("Devotional")
        
    return metadata

# Legacy function for testing
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

# Load all JSON data from the scraped_data directory
@st.cache_data
def load_all_scraped_data(directory="scraped_data"):
    all_videos = []
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    if not json_files:
        return []
        
    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    all_videos.extend(data.get("videos", []))
                elif isinstance(data, list):
                    all_videos.extend(data)
        except Exception as e:
            st.warning(f"⚠️ Could not load {json_path}: {e}")
            
    return deduplicate_videos(all_videos)

# Cache the embeddings model
@st.cache_resource
def get_embeddings():
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available():
        device = "mps"
    
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

def create_faiss_vector_store(texts, path="faiss_index"):
    embeddings = get_embeddings()
    vector_store = FAISS.from_texts(texts, embedding=embeddings)
    vector_store.save_local(path)

@st.cache_resource
def load_faiss_vector_store(path="faiss_index"):
    embeddings = get_embeddings()
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# Reusable function to rebuild the index
def perform_rebuild(videos):
    if not videos:
        return False
        
    texts = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, video in enumerate(videos):
        if i % 500 == 0:
            progress = (i / len(videos))
            progress_bar.progress(progress)
            status_text.text(f"📝 Indexing video {i}/{len(videos)}...")
            
        raw_title = video.get("title", "")
        title = clean_title(raw_title)
        desc = str(video.get("description", ""))
        
        # Enhanced metadata extraction
        meta = extract_metadata(desc, title)
        singers = ", ".join(meta["singers"]) if meta["singers"] else "N/A"
        tags = ", ".join(meta["tags"]) if meta["tags"] else "General"
        
        published_at = video.get("published_at", "")
        year = published_at[:4] if published_at else "Unknown"
        
        # Use inference logic for channel name
        channel = infer_channel_name(video)

        text = (
            f"TITLE: {title}\n"
            f"SINGERS: {singers}\n"
            f"MOVIE: {meta['movie']}\n"
            f"TAGS: {tags}\n"
            f"CHANNEL: {channel}\n"
            f"YEAR: {year}\n"
            f"VIEWS: {video.get('view_count', 0)}\n"
            f"DESCRIPTION: {desc[:500]}\n\n"
        )
        texts.append(text)

    create_faiss_vector_store(texts)
    progress_bar.progress(1.0)
    status_text.text("✅ Magic Knowledge Base Rebuilt!")
    return True

# Check if rebuild needed
def check_rebuild_needed(directory="scraped_data", index_path="faiss_index"):
    if not os.path.exists(index_path): return True, "Index missing"
    json_files = glob.glob(os.path.join(directory, "*.json"))
    if not json_files: return False, "No data"
    latest_data_time = max(os.path.getmtime(f) for f in json_files)
    index_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(index_file): return True, "Index file missing"
    if latest_data_time > os.path.getmtime(index_file): return True, "New data detected"
    return False, "Up to date"

# --- UI Header ---
st.markdown("<h1 style='text-align: center; color: #E50914;'>✨ Bollywood Magic Dashboard ✨</h1>", unsafe_allow_html=True)

# Data Management
try:
    rebuild_required, reason = check_rebuild_needed()
    with st.sidebar:
        st.header("⚙️ Data Engine")
        st.write(f"Status: **{reason}**")
        if st.button("🔄 Rebuild Everything", type="primary"):
            import shutil
            if os.path.exists("faiss_index"): shutil.rmtree("faiss_index")
            st.cache_data.clear()
            st.cache_resource.clear()
            st.rerun()

    if not os.path.exists("faiss_index"):
        videos = load_all_scraped_data()
        if perform_rebuild(videos): st.rerun()
except Exception as e:
    st.error(f"Error: {e}")

# Helper to infer channel name from description for legacy data
def infer_channel_name(row):
    # Support both dict and pandas Series
    channel_name = row.get('channel_name') if isinstance(row, dict) else row['channel_name']
    
    if channel_name and str(channel_name).strip() != "" and str(channel_name).lower() != "nan":
        return channel_name
    
    title = row.get('title', '') if isinstance(row, dict) else row['title']
    description = row.get('description', '') if isinstance(row, dict) else row['description']
    
    desc_title = f"{title} {description}".lower()
    if "t-series" in desc_title: return "T-Series"
    if "zee music" in desc_title: return "Zee Music Company"
    if "sony music" in desc_title: return "Sony Music India"
    if "tips" in desc_title: return "Tips Music"
    if "saregama" in desc_title: return "Saregama Music"
    if "eros now" in desc_title: return "Eros Now"
    if "yrf" in desc_title or "yash raj" in desc_title: return "YRF"
    
    return "Other/Legacy"

# Load Data for Visuals
all_videos = load_all_scraped_data()
df = pd.DataFrame(all_videos)

if not df.empty:
    # Fix missing channel names
    if 'channel_name' not in df.columns:
        df['channel_name'] = None
    df['channel_name'] = df.apply(infer_channel_name, axis=1)
    
    # Ensure view_count is numeric
    df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce').fillna(0)

# Tabs
tab1, tab2 = st.tabs(["🤖 Bollywood Genius Bot", "📈 Magic Analytics Dashboard"])

with tab2:
    st.header("📊 Real-time Bollywood Insights")
    if not df.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Videos Indexed", f"{len(df):,}")
        with col2:
            st.metric("Total Views Captured", f"{df['view_count'].sum():,}")
        with col3:
            st.metric("Top Channel", df['channel_name'].value_counts().idxmax())
            
        # Charts
        c1, c2 = st.columns(2)
        with c1:
            # Views by Channel
            fig = px.pie(df, values='view_count', names='channel_name', title='View Distribution by Label', hole=.3)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            # Monthly Scraping Trend
            df['pub_date'] = pd.to_datetime(df['published_at'])
            df_month = df.groupby(df['pub_date'].dt.to_period('M')).size().reset_index(name='count')
            df_month['pub_date'] = df_month['pub_date'].astype(str)
            fig2 = px.bar(df_month, x='pub_date', y='count', title='Videos Published per Month', color_discrete_sequence=['#E50914'])
            st.plotly_chart(fig2, use_container_width=True)
            
        # Artist Table (Extract from titles for quick display)
        st.subheader("🔥 Top Trending Artists (detected in title)")
        artists = ["Arijit Singh", "Honey Singh", "Badshah", "Shreya Ghoshal", "Sunny Leone", "Neha Kakkar"]
        artist_stats = []
        for a in artists:
            count = df[df['title'].str.contains(a, case=False, na=False)].shape[0]
            views = df[df['title'].str.contains(a, case=False, na=False)]['view_count'].sum()
            artist_stats.append({"Artist": a, "Videos": count, "Total Views": views})
        
        st.table(pd.DataFrame(artist_stats).sort_values("Total Views", ascending=False))

with tab1:
    st.info("I am the Bollywood Genius. I know every singer, label, and hidden track. Ask me anything!")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        
    vector_store = load_faiss_vector_store()
    question = st.text_input("🎤 Ask your Bollywood Genius (e.g., 'Find me latest Honey Singh rap songs'):")

    BOT_NAME = "GeniusBot"

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        
        # Enhanced retrieval query
        retrieval_query = question
        if "rap" in question.lower(): retrieval_query += " rap hip-hop Honey Singh Badshah"
        
        retriever = vector_store.as_retriever(search_kwargs={"k": 12})
        docs = retriever.invoke(retrieval_query)
        context = "\n---\n".join([doc.page_content for doc in docs])

        prompt = f"Context:\n{context}\n\nQuestion: {question}"

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": (
                        f"You are {BOT_NAME}, an expert Bollywood Analyst and Genius. "
                        "You have access to a database of 14,000+ videos. "
                        "NEVER say you don't have information if there is even a slight mention in the context. "
                        "NEVER suggest checking YouTube or Spotify—provide the details HERE. "
                        "Identify Artists, Singers, and Labels clearly. "
                        "If asked about 'rap', look for artists like Honey Singh or Badshah in the context. "
                        "If the date is 2026, celebrate it as a futuristic hit!"
                    )
                },
                {"role": "user", "content": prompt}
            ],
            model=MODEL_NAME,
        )
        
        answer = chat_completion.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    # Fancy chat display
    for msg in reversed(st.session_state.chat_history):
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant", avatar="🎬").write(msg["content"])

# Footer
st.markdown("<hr><p style='text-align: center;'>Magic Engine Powered by Groq & Gemini CLI | © 2026 Bollywood Genius</p>", unsafe_allow_html=True)
