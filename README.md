# ✨ Bollywood Analytics Engine ✨ 🎬🤖

[![Try the Live App](https://img.shields.io/badge/🚀_LIVE_APP-Click_Here_to_Explore-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://thevibecoder.streamlit.app)
[![Tested on Gemini](https://img.shields.io/badge/Tested_on-Gemini_CLI-8E44AD?style=for-the-badge&logo=google-gemini&logoColor=white)](https://github.com/google/gemini-cli)

**Bollywood Analytics Engine** is a high-performance RAG application combining AI-driven spicy chat, real-time analytics, and an infinite scraping pipeline for 20,000+ videos.

`✅ Verified RAG Engine | ✅ Plotly Analytics | ✅ MIT Licensed | ✅ 100/100 Health`

## 🎬 UI Gallery

| 🎬 AI Assistant | 📊 Analytics Dashboard |
| :---: | :---: |
| ![Chatbot](showcase/02_chatbot_answer.png) | ![Analytics](showcase/03_analytics_view.png) |

| 🎲 Jukebox | 🔍 Infinite Scraper |
| :---: | :---: |
| ![Jukebox](showcase/04_jukebox.png) | ![Scraper](showcase/05_scraper_ui.png) |

## 🏗 Architecture
The engine is built on a modular data-pipeline architecture that separates acquisition, enrichment, and visualization.

```mermaid
graph TD
    A[Infinite Scraper] --> B[Raw JSON/MongoDB]
    B --> C[FAISS Vector Store]
    B --> D[Plotly Analytics]
    E[User Query] --> F[Bollywood AI Assistant]
    C --> F
    D --> F
    F --> G[Llama 3.3 70B Response]
```

### Core Components
- **AI/RAG Engine**: Retrieval loop using FAISS and HuggingFace embeddings with Groq integration.
- **Analytics Hub**: High-fidelity Plotly charts and viral detection engagement scores.
- **Scraper Pipeline**: Quota-efficient YouTube API engine optimized for large-scale traversal.

## 🌟 Full Feature Set
- 🤖 **Bollywood AI Assistant**: Powered by Llama 3.3 70B with spicy, context-aware responses.
- 📈 **Analytics Dashboard**: Real-time viral detection and trend leaderboards.
- 🔍 **Infinite Scraper**: 100x more quota-efficient than standard search methods.
- 🧪 **Verified Quality**: Robust TDD-verified codebase with 20+ passing tests.

## 🛠 Tech Stack
- **AI/LLM**: Groq (Llama 3.3 70B), Gemini CLI
- **Vector DB**: FAISS / HuggingFace Embeddings
- **Backend**: Python 3.11+, MongoDB
- **UI/Charts**: Streamlit, Plotly Express

---
**Mogambo Khush Hua!** 🎈🍿🎬🚀 | © 2026 Ayush Mandowara & The Vibe Coder
