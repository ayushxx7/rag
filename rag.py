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

from yt_scrape.utils import clean_title, deduplicate_videos, prepare_leaderboard, calculate_engagement_score

# Set page config for a wider dashboard look
st.set_page_config(page_title="Bollywood Analytics | Ayush Mandowara & The Vibe Coder", layout="wide", page_icon="🎬")

# Load environment variables
load_dotenv()

# Configure Groq
API_KEY = os.getenv('GROQ_API_KEY', 'SET YOUR OWN API KEY')
client = Groq(api_key=API_KEY)
MODEL_NAME = "llama-3.3-70b-versatile"

# Helper to infer channel name from description for legacy data
def infer_channel_name(row):
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

# Helper to extract artist/singer/movie from description
def extract_metadata(text, title):
    metadata = {"singers": [], "movie": "Unknown", "tags": []}
    singer_match = re.search(r"Singer[s]?:\s*([^\n|]+)", text, re.IGNORECASE)
    if singer_match:
        metadata["singers"] = [s.strip() for s in re.split(r",|&", singer_match.group(1))]
    movie_match = re.search(r"Movie:\s*([^\n|]+)", text, re.IGNORECASE)
    if movie_match:
        metadata["movie"] = movie_match.group(1).strip()
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
    videos = json_data.get("videos", []) if isinstance(json_data, dict) else json_data
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

@st.cache_data
def load_all_scraped_data(directory="scraped_data"):
    all_videos = []
    json_files = glob.glob(os.path.join(directory, "*.json"))
    if not json_files: return []
    for json_path in json_files:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict): all_videos.extend(data.get("videos", []))
                elif isinstance(data, list): all_videos.extend(data)
        except Exception as e: st.warning(f"⚠️ Could not load {json_path}: {e}")
    return deduplicate_videos(all_videos)

@st.cache_resource
def get_embeddings():
    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cpu" and torch.backends.mps.is_available(): device = "mps"
    return HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device': device})

def create_faiss_vector_store(texts, path="faiss_index"):
    vector_store = FAISS.from_texts(texts, embedding=get_embeddings())
    vector_store.save_local(path)

@st.cache_resource
def load_faiss_vector_store(path="faiss_index"):
    return FAISS.load_local(path, get_embeddings(), allow_dangerous_deserialization=True)

def perform_rebuild(videos):
    if not videos: return False
    texts = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    for i, video in enumerate(videos):
        if i % 500 == 0:
            progress_bar.progress(i / len(videos))
            status_text.text(f"📝 Indexing video {i}/{len(videos)}...")
        raw_title = video.get("title", "")
        title = clean_title(raw_title)
        desc = str(video.get("description", ""))
        meta = extract_metadata(desc, title)
        singers = ", ".join(meta["singers"]) if meta["singers"] else "N/A"
        tags = ", ".join(meta["tags"]) if meta["tags"] else "General"
        published_at = video.get("published_at", "")
        year = published_at[:4] if published_at else "Unknown"
        # Use inference logic for channel name
        channel = infer_channel_name(video)
        
        # Calculate engagement score for "Viral" detection
        viral_score = calculate_engagement_score(
            video.get('view_count', 0), 
            video.get('like_count', 0), 
            video.get('comment_count', 0)
        )

        text = f"TITLE: {title}\nSINGERS: {singers}\nMOVIE: {meta['movie']}\nTAGS: {tags}\nCHANNEL: {channel}\nYEAR: {year}\nVIEWS: {video.get('view_count', 0)}\nVIRAL SCORE: {viral_score}\nDESCRIPTION: {desc[:500]}\n\n"
        texts.append(text)
    create_faiss_vector_store(texts)
    progress_bar.progress(1.0)
    status_text.text("✅ Knowledge Base Rebuilt!")
    return True

def check_rebuild_needed(directory="scraped_data", index_path="faiss_index"):
    if not os.path.exists(index_path): return True, "Index missing"
    json_files = glob.glob(os.path.join(directory, "*.json"))
    if not json_files: return False, "No data"
    latest_data_time = max(os.path.getmtime(f) for f in json_files)
    index_file = os.path.join(index_path, "index.faiss")
    if not os.path.exists(index_file): return True, "Index file missing"
    if latest_data_time > os.path.getmtime(index_file): return True, "New data detected"
    return False, "Up to date"

# --- UI LOGIC ---
st.markdown("<h1 style='text-align: center; color: #E50914;'>✨ Bollywood Analytics Engine ✨</h1>", unsafe_allow_html=True)

rebuild_required, reason = check_rebuild_needed()
with st.sidebar:
    st.header("⚙️ Data Engine")
    if st.button("🎭 Mogambo Khush Hua!", use_container_width=True):
        st.balloons()
        st.toast("Super Hit! 🍿🎬")
    if st.button("🔄 Rebuild Everything", type="primary", use_container_width=True):
        import shutil
        if os.path.exists("faiss_index"): shutil.rmtree("faiss_index")
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    st.divider()
    st.header("🎯 Filters")
    view_range = st.slider("Min Views filter", 0, 10000000, 0, 100000)
    top_n = st.select_slider("Leaderboard Depth", options=[3, 5, 10, 15, 20], value=5)
    st.divider()
    st.header("💡 Filmy Fun Fact")
    facts = [
        "Arijit Singh is the most-followed Indian artist globally!",
        "Diljit Dosanjh was the first Punjabi artist at Coachella.",
        "Shreya Ghoshal has 5 National Film Awards.",
        "Indie-pop is now rivaling Bollywood tracks for #1!"
    ]
    st.info(random.choice(facts))

if not os.path.exists("faiss_index"):
    videos = load_all_scraped_data()
    if perform_rebuild(videos): st.rerun()

all_videos = load_all_scraped_data()
df = pd.DataFrame(all_videos)
if not df.empty:
    df['channel_name'] = df.apply(infer_channel_name, axis=1)
    df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce').fillna(0)

tab1, tab2 = st.tabs(["🤖 Bollywood AI Assistant", "📈 Analytics"])

with tab2:
    if not df.empty:
        filtered_df = df[df['view_count'] >= view_range]
        mood = st.radio("Vibe Picker:", ["All", "Party/Dance", "Emotional/Sad", "Rap/Hip-Hop", "Devotional"], horizontal=True)
        if mood != "All":
            pattern = '|'.join(mood.lower().split('/'))
            filtered_df = filtered_df[filtered_df['title'].str.contains(pattern, case=False, na=False) | filtered_df['description'].str.contains(pattern, case=False, na=False)]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Videos", f"{len(filtered_df):,}")
        c2.metric("Views", f"{filtered_df['view_count'].sum():,}")
        c3.metric("Top Label", filtered_df['channel_name'].value_counts().idxmax() if not filtered_df.empty else "N/A")
        
        col_a, col_b = st.columns(2)
        fig = px.pie(filtered_df, values='view_count', names='channel_name', title='View Distribution', hole=.3)
        col_a.plotly_chart(fig, use_container_width=True)
        filtered_df['pub_date'] = pd.to_datetime(filtered_df['published_at'])
        df_month = filtered_df.groupby(filtered_df['pub_date'].dt.to_period('M')).size().reset_index(name='count')
        df_month['pub_date'] = df_month['pub_date'].astype(str)
        fig2 = px.bar(df_month, x='pub_date', y='count', title='Velocity', color_discrete_sequence=['#E50914'])
        col_b.plotly_chart(fig2, use_container_width=True)
        
        # Artist Table and Viral Table
        col_art, col_vir = st.columns(2)
        
        with col_art:
            st.subheader(f"🔥 Top {top_n} Trending Artists")
            artists = ["Arijit Singh", "Diljit Dosanjh", "Shreya Ghoshal", "Jubin Nautiyal", "Karan Aujla", "Vishal Mishra", "Neha Kakkar", "Sonu Nigam", "Badshah"]
            artist_stats = []
            for a in artists:
                a_df = filtered_df[filtered_df['title'].str.contains(a, case=False, na=False)]
                if not a_df.empty: artist_stats.append({"Artist": a, "Videos": len(a_df), "Total Views": a_df['view_count'].sum()})
            if artist_stats: st.dataframe(prepare_leaderboard(artist_stats).head(top_n), hide_index=True, use_container_width=True)

        with col_vir:
            st.subheader("🚀 Viral Hits (High Engagement)")
            if not filtered_df.empty:
                # Add score for display
                filtered_df['Viral Score'] = filtered_df.apply(
                    lambda x: calculate_engagement_score(x['view_count'], x.get('like_count', 0), x.get('comment_count', 0)), 
                    axis=1
                )
                viral_df = filtered_df.sort_values("Viral Score", ascending=False).head(5)
                st.dataframe(viral_df[['title', 'Viral Score', 'channel_name']], hide_index=True, use_container_width=True)

with tab1:
    st.info("I am your personal Bollywood AI Assistant. Ask me anything!")
    mood_vibe = st.selectbox("🎭 Mood Vibe", options=["Sad", "Chill", "Romantic", "Party", "Aggressive"], index=2)
    
    col_j, col_s = st.columns(2)
    with col_j.expander("🎲 Jukebox"):
        if st.button("Shuffle & Pick!"):
            rv = df.sample(1).iloc[0]
            st.write(f"🎵 {rv['title']}")
            if rv.get('thumbnail_url'): st.image(rv['thumbnail_url'], width=250)
            
    with col_s.expander("🌟 Artist Spotlight"):
        sa = st.selectbox("Pick an Artist:", artists)
        if st.button("Spotlight!"):
            with st.spinner("Searching..."):
                res = client.chat.completions.create(messages=[{"role": "user", "content": f"Filmy Spotlight for {sa} in 2026. 2 sentences. Emojis!"}], model=MODEL_NAME)
                st.success(res.choices[0].message.content)

    if "chat_history" not in st.session_state: st.session_state.chat_history = []
    vector_store = load_faiss_vector_store()
    question = st.text_input("🎤 Ask your Bollywood Genius:", placeholder=f"Ask about a {mood_vibe} song...")

    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        retriever = vector_store.as_retriever(search_kwargs={"k": 12})
        docs = retriever.invoke(f"{question} {mood_vibe} mood")
        context = "\n---\n".join([doc.page_content for doc in docs])
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are GeniusBot, a Bollywood Analyst. NEVER say you don't know if context has a mention. Provide details HERE. If date is 2026, celebrate it!"},
                      {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}],
            model=MODEL_NAME,
        )
        st.session_state.chat_history.append({"role": "assistant", "content": chat_completion.choices[0].message.content})

    for msg in reversed(st.session_state.chat_history):
        st.chat_message(msg["role"], avatar="🎬" if msg["role"]=="assistant" else None).write(msg["content"])

st.markdown("<hr><p style='text-align: center;'>Magic Engine Powered by Groq & Gemini CLI | © 2026 Ayush Mandowara & The Vibe Coder</p>", unsafe_allow_html=True)
