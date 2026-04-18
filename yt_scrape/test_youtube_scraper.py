import pytest
from unittest.mock import MagicMock, patch
from yt_scrape.youtube_scraper import YouTubeScraper
from datetime import datetime, timedelta

@pytest.fixture
def mock_api_key():
    return "MOCK_API_KEY"

@pytest.fixture
def scraper(mock_api_key):
    with patch('yt_scrape.youtube_scraper.build') as mock_build:
        yield YouTubeScraper(mock_api_key)

def test_scraper_init(mock_api_key):
    with patch('yt_scrape.youtube_scraper.build') as mock_build:
        scraper = YouTubeScraper(mock_api_key)
        mock_build.assert_called_once_with('youtube', 'v3', developerKey=mock_api_key)
        assert scraper.api_key == mock_api_key
        assert scraper.quota_used == 0

def test_get_channel_id_from_name(scraper):
    mock_response = {
        'items': [{'id': {'channelId': 'UC12345'}}]
    }
    scraper.youtube.search().list().execute.return_value = mock_response
    
    channel_id = scraper.get_channel_id_from_name('@TSeries')
    
    assert channel_id == 'UC12345'
    assert scraper.quota_used == 100
    scraper.youtube.search().list.assert_called_with(
        q='TSeries',
        type='channel',
        part='id,snippet',
        maxResults=5
    )

def test_get_channel_info(scraper):
    mock_response = {
        'items': [{
            'snippet': {'title': 'T-Series', 'description': 'Music label'},
            'statistics': {'subscriberCount': '200000000', 'videoCount': '20000', 'viewCount': '1000000000'}
        }]
    }
    scraper.youtube.channels().list().execute.return_value = mock_response
    
    info = scraper.get_channel_info('UC12345')
    
    assert info['channel_name'] == 'T-Series'
    assert info['subscriber_count'] == '200000000'
    assert scraper.quota_used == 1

def test_get_uploads_playlist_id(scraper):
    mock_response = {
        'items': [{
            'contentDetails': {
                'relatedPlaylists': {
                    'uploads': 'UU12345'
                }
            }
        }]
    }
    scraper.youtube.channels().list().execute.return_value = mock_response
    
    playlist_id = scraper.get_uploads_playlist_id('UC12345')
    
    assert playlist_id == 'UU12345'

@patch('yt_scrape.youtube_scraper.YouTubeScraper.get_uploads_playlist_id')
@patch('yt_scrape.youtube_scraper.YouTubeScraper.get_videos_from_playlist')
def test_get_channel_videos_via_playlist(mock_get_videos, mock_get_playlist, scraper):
    mock_get_playlist.return_value = 'UU12345'
    mock_get_videos.return_value = [{'video_id': 'vid1'}]
    
    videos = scraper.get_channel_videos('UC12345', published_after='2025-01-01T00:00:00Z', published_before='2025-12-31T23:59:59Z')
    
    assert len(videos) == 1
    assert videos[0]['video_id'] == 'vid1'
    mock_get_playlist.assert_called_once_with('UC12345')
    mock_get_videos.assert_called_with('UU12345', 50, '2025-01-01T00:00:00Z', '2025-12-31T23:59:59Z', None)

def test_get_videos_from_playlist_filtering(scraper):
    mock_response = {
        'items': [
            {
                'snippet': {
                    'publishedAt': '2025-06-01T00:00:00Z',
                    'resourceId': {'videoId': 'vid1'},
                    'title': 'Video 1',
                    'description': 'Desc 1',
                    'channelId': 'UC12345',
                    'thumbnails': {}
                }
            },
            {
                'snippet': {
                    'publishedAt': '2024-06-01T00:00:00Z',
                    'resourceId': {'videoId': 'vid2'},
                    'title': 'Video 2',
                    'description': 'Desc 2',
                    'channelId': 'UC12345',
                    'thumbnails': {}
                }
            }
        ]
    }
    scraper.youtube.playlistItems().list().execute.return_value = mock_response
    
    # Mock video statistics
    with patch('yt_scrape.youtube_scraper.YouTubeScraper.get_video_statistics') as mock_stats:
        mock_stats.return_value = {
            'vid1': {'view_count': 100, 'like_count': 10, 'comment_count': 1, 'duration': 'PT1M'}
        }
        
        # Filter for only 2025
        videos = scraper.get_videos_from_playlist('UU12345', published_after='2025-01-01T00:00:00Z')
        
        assert len(videos) == 1
        assert videos[0]['video_id'] == 'vid1'
        assert videos[0]['published_at'] == '2025-06-01T00:00:00Z'

def test_get_video_statistics(scraper):
    mock_response = {
        'items': [{
            'id': 'vid1',
            'statistics': {'viewCount': '1000', 'likeCount': '100', 'commentCount': '10'},
            'contentDetails': {'duration': 'PT5M30S'}
        }]
    }
    scraper.youtube.videos().list().execute.return_value = mock_response
    
    stats = scraper.get_video_statistics(['vid1'])
    
    assert 'vid1' in stats
    assert stats['vid1']['view_count'] == 1000
    assert stats['vid1']['like_count'] == 100
    assert stats['vid1']['duration'] == 'PT5M30S'
