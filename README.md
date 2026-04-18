# ✨ Bollywood Analytics Engine ✨ 🎬🤖

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_svg.svg)](https://thevibecoder.streamlit.app)

A personal pet project by **Ayush Mandowara & The Vibe Coder company**. This project combines a **Personal AI Chatbot**, a **Real-time Analytics Dashboard**, and an **Infinite YouTube Scraper** into one seamless experience.

Developed and architected with the power of **Gemini CLI** 🚀

---

## 🌟 Full Feature Set

### 🤖 1. Bollywood AI Assistant (RAG)
- **State-of-the-Art LLM**: Powered by **Llama 3.3 70B (Groq)** for lightning-fast, spicy, and context-aware responses.
- **Vibe-o-Meter**: A dynamic mood selector (**Sad, Chill, Romantic, Party, Aggressive**) that automatically refines vector search results.
- **Deep Context Retrieval**: Uses **FAISS** and **HuggingFace** to search through 14,000+ videos.
- **Artist Spotlight**: Generates instant AI biographies for trending singers including their 2026 status.
- **Smart Query Expansion**: Automatically injects genre-specific keywords (e.g., Rap, Hip-Hop) to find the best hits.
- **Persistent Chat History**: Maintains a sliding-window context for long, engaging conversations.

### 📈 2. Analytics Dashboard
- **Real-time Metrics**: Instant visibility into total views, video counts, and top labels.
- **Viral Detection Engine**: A custom **Engagement Score** algorithm (Weighted Likes/Comments vs Views) to find the next big hit.
- **Interactive Visuals**: High-quality **Plotly** charts for view distribution and publishing velocity.
- **Trending Leaderboard**: A ranked, TDD-verified view of the most popular artists in your dataset.
- **Advanced Filtering**: Use sidebar sliders to filter the entire dashboard by minimum view count or specific artist depth.

### 🔍 3. Infinite YouTube Scraper
- **Uploads Playlist Method**: 100x more quota-efficient than standard search; can fetch 20,000+ videos with minimal API cost.
- **Multi-Channel Support**: Pre-configured for T-Series, Zee Music, Sony, Tips, and Saregama.
- **AI-Powered Search**: Uses Groq to transform natural language into optimized YouTube API queries.
- **Incremental Progress**: Real-time Streamlit progress tracking with batch statistics.

### 🗄️ 4. Robust Data & Storage
- **Dual-Stream Storage**: Simultaneously saves to local **JSON files** and **MongoDB**.
- **Auto-Sync Knowledge Base**: Detects new scraped data via timestamp comparison and prompts for an automatic FAISS rebuild.
- **Smart Metadata Engine**: Automatically extracts **Singers**, **Movies**, and **Tags** from raw video descriptions.
- **Data Integrity**: Integrated TDD-verified title cleaning and video deduplication pipeline.

---

## 📸 UI Gallery
*(Run the `capture_ui.py` script to generate these high-res visuals)*

| 🎬 AI Assistant | 📊 Analytics Dashboard |
| :---: | :---: |
| ![Chatbot](showcase/02_chatbot_answer.png) | ![Analytics](showcase/03_analytics_view.png) |

| 🎲 Jukebox | 🔍 Infinite Scraper |
| :---: | :---: |
| ![Jukebox](showcase/04_jukebox.png) | ![Scraper](showcase/05_scraper_ui.png) |

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/ayushxx7/rag.git
cd rag
pip install -r requirements.txt
playwright install  # Required for automated screenshots
```

### 2. Configure Environment
Create a `.env` file:
```env
GROQ_API_KEY=your_key
YOUTUBE_API_KEY=your_key
MONGODB_URI=mongodb://localhost:27017/  # Optional
```

### 3. Launch the App
```bash
# Start the Dashboard & Bot
streamlit run rag.py

# Start the Scraper UI
streamlit run yt_scrape/app.py --server.port 8502
```

---

## 🧪 Verified Quality
We maintain a robust **TDD-verified** codebase with 20+ passing tests:
- `yt_scrape/test_utils.py`: Cleaning, deduplication, and engagement math.
- `yt_scrape/test_youtube_scraper.py`: API interaction and playlist traversal.
- `test_rag.py`: Retrieval and vector store integrity.

Run the suite:
```bash
PYTHONPATH=. pytest
```

---

## 🏗️ Tech Stack
- **AI/LLM**: Groq (Llama 3.3 70B), Gemini CLI
- **Vector DB**: FAISS
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Backend**: Python 3.11+, MongoDB
- **UI/Charts**: Streamlit, Plotly Express
- **Automation**: Playwright

---

**Mogambo Khush Hua!** 🎈🍿🎬🚀 | © 2026 Ayush Mandowara & The Vibe Coder
