import pytest
from yt_scrape.utils import clean_title, deduplicate_videos

def test_clean_title_removes_channel_suffixes():
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
