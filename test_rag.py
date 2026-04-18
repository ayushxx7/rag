import pytest
import os
from unittest.mock import MagicMock, patch

# Set environment variable before importing rag
os.environ["GROQ_API_KEY"] = "mock_key"

import rag
from rag import extract_text_from_json, get_embeddings, create_faiss_vector_store, load_faiss_vector_store
from langchain_huggingface import HuggingFaceEmbeddings

def test_extract_text_from_json():
    mock_json = {
        "videos": [
            {
                "title": "Video 1",
                "description": "Desc 1",
                "view_count": 100,
                "like_count": 10,
                "comment_count": 5,
                "published_at": "2024-01-01"
            }
        ]
    }
    texts = extract_text_from_json(mock_json)
    assert len(texts) == 1
    assert "Title: Video 1" in texts[0]

def test_get_embeddings_instance():
    # Since it's already cached/instantiated in the module, 
    # we just verify it returns a valid embeddings object.
    embeddings = get_embeddings()
    assert isinstance(embeddings, HuggingFaceEmbeddings)

@patch('rag.FAISS')
def test_create_faiss_vector_store(mock_faiss):
    mock_vs = MagicMock()
    mock_faiss.from_texts.return_value = mock_vs
    
    texts = ["Sample text"]
    path = "test_faiss_index"
    
    create_faiss_vector_store(texts, path=path)
    
    # It should use the cached embeddings
    mock_faiss.from_texts.assert_called_once()
    mock_vs.save_local.assert_called_once_with(path)

@patch('rag.FAISS')
def test_load_faiss_vector_store(mock_faiss):
    mock_vs = MagicMock()
    mock_faiss.load_local.return_value = mock_vs
    
    path = "test_faiss_index"
    vs = load_faiss_vector_store(path=path)
    
    mock_faiss.load_local.assert_called_once()
    assert vs == mock_vs
