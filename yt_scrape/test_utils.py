import pytest
from yt_scrape.utils import clean_title, deduplicate_videos, prepare_leaderboard, calculate_engagement_score
import pandas as pd

def test_calculate_engagement_score():
    # Scenario: 1000 views, 10 likes, 5 comments
    # Formula: (10*10 + 5*50) / (1000/100) = (100 + 250) / 10 = 35.0
    score = calculate_engagement_score(1000, 10, 5)
    assert score == 35.0

def test_calculate_engagement_score_zero_views():
    assert calculate_engagement_score(0, 10, 5) == 0.0

def test_calculate_engagement_score_none_handling():
    assert calculate_engagement_score(None, None, None) == 0.0

def test_prepare_leaderboard():
    input_data = [
        {"Artist": "Artist A", "Total Views": 100},
        {"Artist": "Artist B", "Total Views": 500},
        {"Artist": "Artist C", "Total Views": 300},
    ]
    df = prepare_leaderboard(input_data)
    
    # Check sorting (B should be first)
    assert df.iloc[0]["Artist"] == "Artist B"
    assert df.iloc[1]["Artist"] == "Artist C"
    
    # Check Rank column (should be 1-based)
    assert "Rank" in df.columns
    assert df.iloc[0]["Rank"] == 1
    assert df.iloc[1]["Rank"] == 2
    
    # Check index (should be clean)
    assert df.index[0] == 0

def test_prepare_leaderboard_empty():
    assert prepare_leaderboard([]).empty
    assert prepare_leaderboard(None).empty
    raw_title = "Uyi Amma - Azaad | Zee Music Company"
    expected = "Uyi Amma - Azaad"
    assert clean_title(raw_title) == expected

def test_clean_title_removes_extra_whitespace():
    raw_title = "  Song Title   "
    expected = "Song Title"
    assert clean_title(raw_title) == expected

def test_clean_title_handles_none():
    assert clean_title(None) == ""

def test_deduplicate_videos():
    input_videos = [
        {"video_id": "1", "title": "Video 1"},
        {"video_id": "2", "title": "Video 2"},
        {"video_id": "1", "title": "Video 1 Duplicate"}, # Same ID, different title (should keep first)
    ]
    expected = [
        {"video_id": "1", "title": "Video 1"},
        {"video_id": "2", "title": "Video 2"},
    ]
    result = deduplicate_videos(input_videos)
    assert len(result) == 2
    assert result == expected

def test_deduplicate_videos_empty():
    assert deduplicate_videos([]) == []
    assert deduplicate_videos(None) == []
