# rag
retrieval augment generation (rag) streamlit (st) based web app with chatbot support from Gemini

# about
- upload youtube_videos data of format (mentioned below).
- ask queries after local faiss index store is created.

# under the hood
- uses `sentence-transformers` from HuggingFace to embed queries and data
- uses `faiss` for creating vector store for querying
- uses `gemini` for good quality and scoped Q&A
- uses `streamlit` for the web interface

# sample queries
![IMG-20250511-WA0063](https://github.com/user-attachments/assets/179f43e4-ae3e-4ad1-ba7a-d5a724f2cf65)

![IMG-20250511-WA0062](https://github.com/user-attachments/assets/d682e79b-e61a-44e5-bb9f-2d30ff674769)
