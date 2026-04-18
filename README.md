# ✨ Bollywood Magic Dashboard ✨ 🎬🤖

A high-performance, full-stack Bollywood command center! This application transforms over **14,000 YouTube videos** into a searchable, interactive, and intelligent knowledge base using **Retrieval Augmented Generation (RAG)** and real-time data analytics.

Developed and rebuilt with the power of **Gemini CLI** 🚀

---

## 🌟 Supercharged Features

### 🤖 Bollywood Genius Bot
- **Llama 3.3 70B (Groq)**: Blazing fast, context-aware answers with a spicy "filmy" personality.
- **🎭 Vibe-o-Meter**: Select your mood (**Sad, Chill, Romantic, Party, Aggressive**) to dynamically influence search results.
- **🌟 Artist Spotlight**: Interactive tool that generates AI bios for trending singers (Diljit, Arijit, Karan Aujla) and their 2026 status.
- **🎲 Magic Jukebox**: A random song picker with thumbnails to discover hidden hits.

### 📈 Magic Analytics Dashboard
- **Real-time Insights**: Track total views, video count, and publishing velocity across major labels (T-Series, Zee, Sony, etc.).
- **🚀 Viral Detection**: Implemented a TDD-verified **Engagement Score** algorithm to identify high-quality trending content.
- **🏆 Trending Leaderboard**: A ranked view of the top singers by cumulative views.
- **🎯 Dynamic Filters**: Sliders for view-count ranges and radio buttons for genre/mood filtering.

### 🔍 Infinite Scraper Engine
- **Playlist Uploads API**: High-efficiency scraping capable of fetching 10,000+ videos while saving 99% of API quota.
- **Auto-Sync Knowledge Base**: The system automatically detects new scraped files and prompts for a vector store update.
- **Smart Data Cleaning**: TDD-verified title cleaning and video deduplication pipeline.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/ayushxx7/rag.git
cd rag
pip install -r requirements.txt
playwright install  # Optional: For automated screenshots
```

### 2. Configure `.env`
```env
GROQ_API_KEY=your_key
YOUTUBE_API_KEY=your_key
```

### 3. Launch the Magic
```bash
# Start the Dashboard & Bot
streamlit run rag.py

# Start the Scraper UI (Separate port)
streamlit run yt_scrape/app.py --server.port 8502
```

---

## 🏗️ Architecture & Tech Stack

- **LLM**: Groq (Llama 3.3 70B Versatile)
- **Vector DB**: FAISS
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Frontend**: Streamlit (Interactive UI)
- **Visualization**: Plotly Express
- **Language**: Python 3.11+
- **Testing**: Pytest (20+ verified tests)

---

## 🧪 Verified Quality
We maintain a robust **TDD-verified** codebase:
- `yt_scrape/test_utils.py`: Tests for cleaning, deduplication, and engagement math.
- `yt_scrape/test_youtube_scraper.py`: Tests for API interaction and playlist traversal.
- `test_rag.py`: Tests for retrieval and vector store integrity.

Run them all with:
```bash
PYTHONPATH=. pytest
```

---

## ❤️ Credits
- Built with ❤️ for Bollywood fans.
- Powered by **Groq**, **HuggingFace**, and **Gemini CLI**.
- Data sourced from **YouTube Data API v3**.

---

**Mogambo Khush Hua!** 🎈🍿✨
