# 🎥 Bollywood Hungama Chatbot & Data Engine 🎬✨

A powerful, full-stack Bollywood-themed application combining **Retrieval Augmented Generation (RAG)** with a **High-Performance YouTube Scraper**. Chat with a fun AI bot about your favorite Bollywood videos and scrape the latest data directly from YouTube!

---

## 🌟 Features

### 🤖 Bollywood RAG Chatbot
- **Smart Conversations**: Uses **Groq (Llama 3.3 70B)** for high-quality, context-aware answers with a fun Bollywood flair.
- **Fast Retrieval**: Powered by **FAISS** vector store and **HuggingFace sentence-transformers** for semantic search.
- **Dynamic Knowledge**: Automatically builds an index from `youtube_videos.json`.
- **Themed UI**: A stylish Streamlit interface with Bollywood colors, emojis, and random movie quotes.

### 🔍 Advanced YouTube Scraper (`yt_scrape`)
- **Unlimited Scraping**: Can scrape all videos from any channel (e.g., T-Series with ~23k videos).
- **Dual Storage**: Simultaneous storage in **JSON files** and **MongoDB**.
- **Date Filtering**: Scrape videos within specific ranges (e.g., only latest 2025-2026 videos).
- **Batch Processing**: Efficient handling of large datasets with real-time progress tracking.
- **AI-Powered Search**: Uses Groq to transform natural language prompts into optimized YouTube search queries.

---

## 🚀 Setup & Installation

### 1. Clone & Install Dependencies
Ensure you have Python 3.11+ installed.

```bash
pip install -r requirements.txt
pip install google-api-python-client  # Add this if not in requirements
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:

```env
# Required for Chatbot
GROQ_API_KEY=your_groq_api_key

# Required for Scraper
YOUTUBE_API_KEY=your_youtube_api_key

# Optional: For Database Storage
MONGODB_URI=mongodb://localhost:27017/
```

### 3. Prepare Initial Data
Place your initial video data in `youtube_videos.json`. If you don't have one, you can use the scraper to generate it.

---

## 🛠️ Usage

### 💬 Option 1: Start the Chatbot
Launch the RAG interface to chat about existing video data:

```bash
streamlit run rag.py
```

### 📊 Option 2: Run the Scraper (UI)
Launch the advanced scraping dashboard to fetch new channel data:

```bash
streamlit run yt_scrape/app.py
```

### 📜 Option 3: Command Line Scraping
Run a pre-configured script to scrape the latest videos from 2025-2026:

```bash
PYTHONPATH=. python3 scrape_2025_2026.py
```

---

## 🧪 Testing

The codebase includes a comprehensive test suite using `pytest`.

```bash
# Run all tests
PYTHONPATH=. pytest

# Run specific module tests
PYTHONPATH=. pytest yt_scrape/test_youtube_scraper.py
PYTHONPATH=. pytest test_rag.py
```

---

## 🏗️ Project Structure

- `rag.py`: Main Streamlit app for the RAG chatbot.
- `yt_scrape/`:
    - `app.py`: Streamlit dashboard for scraping.
    - `youtube_scraper.py`: Core logic for interacting with YouTube API.
    - `data_storage.py`: Logic for saving to JSON and MongoDB.
    - `mongodb_storage.py`: MongoDB-specific database operations.
    - `test_youtube_scraper.py`: Tests for the scraping engine.
- `scrape_2025_2026.py`: Standalone CLI script for focused scraping.
- `youtube_videos.json`: Central data store used by the RAG engine.

---

## 📋 Data Format

The system expects and produces JSON in the following format:

```json
{
    "videos": [
        {
            "video_id": "FZLadzn5i6Q",
            "title": "Uyi Amma - Azaad",
            "description": "Music label details...",
            "published_at": "2025-01-04T14:54:39Z",
            "view_count": 260359258,
            "like_count": 1337731,
            "comment_count": 27287
        }
    ]
}
```

---

## ❤️ Credits
- Built with ❤️ for the Bollywood community.
- AI powered by **Groq** and **HuggingFace**.
- Data sourced from **YouTube Data API v3**.
