import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Add yt_scrape to sys.path for local imports
sys.path.append(os.path.join(os.getcwd(), 'yt_scrape'))

from yt_scrape.youtube_scraper import YouTubeScraper
from yt_scrape.data_storage import DataStorage
import pandas as pd

# Load environment variables from .env
load_dotenv()

def scrape_years_2025_2026():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "your_youtube_api_key_here":
        print("❌ Error: Valid YOUTUBE_API_KEY not found in environment.")
        return

    scraper = YouTubeScraper(api_key)
    storage = DataStorage() # Uses default local storage
    
    # Major Indian Music Labels
    channels = [
        "T-Series",
        "Zee Music Company", 
        "Sony Music India",
        "Tips Music",
        "Saregama Music"
    ]
    
    # We want videos from 2025-01-01 until now
    published_after = "2025-01-01T00:00:00Z"
    
    all_videos = []
    
    for channel_name in channels:
        print(f"🔍 Processing channel: {channel_name}")
        
        # Get channel ID
        channel_id = scraper.get_channel_id_from_name(channel_name)
        if not channel_id:
            print(f"❌ Could not find channel ID for: {channel_name}")
            continue
            
        print(f"✅ Found channel ID: {channel_id}")
        
        # Scrape channel
        # We set max_videos=None for "unlimited" scraping for the date range
        channel_videos = scraper.scrape_channel(
            channel_id,
            published_after=published_after,
            max_videos=None 
        )
        
        if channel_videos:
            print(f"🎉 Scraped {len(channel_videos)} videos from {channel_name}")
            all_videos.extend(channel_videos)
            
            # Save progress incrementally
            storage.store_channel_data(channel_name, channel_videos, {
                'published_after': published_after,
                'scrape_date': datetime.now().isoformat()
            })
        else:
            print(f"⚠️ No videos found for {channel_name} in the specified date range.")

    if all_videos:
        # Save all results to a single file as well
        output_file = f"scraped_videos_2025_2026_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, 'w') as f:
            json.dump(all_videos, f, indent=4)
        print(f"✅ Scraping complete! Total videos: {len(all_videos)}")
        print(f"📂 Results saved to {output_file}")
    else:
        print("❌ No videos were scraped.")

if __name__ == "__main__":
    scrape_years_2025_2026()
