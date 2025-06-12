import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from youtube_scraper import YouTubeScraper
from data_storage import DataStorage
from mongodb_storage import MongoDBStorage
from utils import extract_channel_id, format_number, validate_api_key

# Initialize session state
if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = []
if 'scraper' not in st.session_state:
    st.session_state.scraper = None
if 'storage' not in st.session_state:
    mongodb_uri = os.getenv("MONGODB_URI")
    st.session_state.storage = DataStorage(mongodb_uri=mongodb_uri)

def main():
    st.title("🎥 YouTube Channel Data Scraper")
    st.markdown("Scrape unlimited YouTube channel data with simultaneous JSON and MongoDB storage")
    
    # Add info about unlimited scraping
    with st.expander("ℹ️ About Unlimited Scraping"):
        st.markdown("""
        **Key Features:**
        - **No Video Limits**: Scrape all videos from any channel (T-Series has ~23k videos)
        - **Dual Storage**: Simultaneous storage in JSON files and MongoDB
        - **Batch Processing**: Efficient handling of large datasets
        - **Progress Tracking**: Real-time updates during scraping
        - **Playlist Method**: Uses channel uploads playlist for comprehensive coverage
        - **API Quota Management**: Intelligent quota monitoring to prevent limits
        
        **Recommended for T-Series:**
        - Set "Time Range" to "All Time" 
        - Set "Video Limit" to "No Limit (All Videos)"
        - Use batch size 50 for optimal speed
        """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "YouTube API Key", 
        type="password",
        value=os.getenv("YOUTUBE_API_KEY", ""),
        help="Enter your YouTube Data API v3 key"
    )
    
    if api_key:
        if validate_api_key(api_key):
            if st.session_state.scraper is None:
                st.session_state.scraper = YouTubeScraper(api_key)
            st.sidebar.success("✅ API Key validated")
        else:
            st.sidebar.error("❌ Invalid API Key format")
            return
    else:
        st.sidebar.warning("⚠️ Please enter your YouTube API Key")
        st.info("📋 **Setup Instructions:**\n1. Go to [Google Cloud Console](https://console.cloud.google.com/)\n2. Create a project and enable YouTube Data API v3\n3. Generate an API key\n4. Enter the key in the sidebar")
        return
    
    # Scraping parameters
    st.sidebar.subheader("📊 Scraping Parameters")
    batch_size = st.sidebar.slider("Batch Size", min_value=10, max_value=200, value=50, step=10)
    
    # Date range options
    date_filter = st.sidebar.selectbox(
        "Time Range",
        ["All Time", "Last 30 days", "Last 90 days", "Last 6 months", "Last 1 year", "Last 2 years", "Last 3 years"]
    )
    
    # Convert date filter to days
    days_mapping = {
        "All Time": 0,
        "Last 30 days": 30,
        "Last 90 days": 90,
        "Last 6 months": 180,
        "Last 1 year": 365,
        "Last 2 years": 730,
        "Last 3 years": 1095
    }
    days_back = days_mapping[date_filter]
    
    # Video limit options
    video_limit_option = st.sidebar.selectbox(
        "Video Limit",
        ["No Limit (All Videos)", "1,000 videos", "5,000 videos", "10,000 videos", "Custom"]
    )
    
    if video_limit_option == "Custom":
        max_videos = st.sidebar.number_input("Custom video limit", min_value=100, max_value=50000, value=1000, step=100)
    elif video_limit_option == "No Limit (All Videos)":
        max_videos = None
    else:
        max_videos = int(video_limit_option.split()[0].replace(",", ""))
    
    # MongoDB configuration
    st.sidebar.subheader("🍃 MongoDB Configuration")
    mongodb_uri = st.sidebar.text_input(
        "MongoDB URI (optional)",
        type="password",
        value=os.getenv("MONGODB_URI", ""),
        help="MongoDB connection string for simultaneous storage"
    )
    
    if mongodb_uri and st.session_state.storage.mongodb is None:
        st.session_state.storage.mongodb = MongoDBStorage(mongodb_uri)
        if st.session_state.storage.mongodb.connect():
            st.session_state.storage.mongodb.create_indexes()
    
    # Main interface
    st.header("📝 Channel Input")
    
    # Quick preset for major Indian music labels
    st.subheader("🎵 Quick Presets")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Major Indian Music Labels (5 channels)", type="secondary"):
            preset_channels = [
                "T-Series",
                "Zee Music Company", 
                "Sony Music India",
                "Tips Music",
                "Saregama Music"
            ]
            st.session_state.preset_channels = preset_channels
            st.success(f"✅ Loaded {len(preset_channels)} major Indian music channels")
    
    with col2:
        if st.button("🌟 T-Series Only (All Videos)", type="secondary"):
            st.session_state.preset_channels = ["T-Series"]
            st.success("✅ Ready to scrape ALL T-Series videos")
    
    # Channel input methods
    input_method = st.radio(
        "Choose input method:",
        ["Single Channel", "Multiple Channels", "Upload Channel List", "Use Preset"]
    )
    
    channels_to_scrape = []
    
    if input_method == "Single Channel":
        channel_input = st.text_input(
            "Enter YouTube Channel Name or URL:",
            placeholder="e.g., T-Series, UCq-Fj5jknLsUf-MWSy4_brA, or full URL"
        )
        if channel_input:
            channels_to_scrape = [channel_input.strip()]
    
    elif input_method == "Multiple Channels":
        channel_text = st.text_area(
            "Enter channel names/URLs (one per line):",
            placeholder="T-Series\nZee Music Company\nSony Music India\n...",
            height=150
        )
        if channel_text:
            channels_to_scrape = [ch.strip() for ch in channel_text.split('\n') if ch.strip()]
    
    elif input_method == "Upload Channel List":
        uploaded_file = st.file_uploader(
            "Upload a text file with channel names/URLs",
            type=['txt'],
            help="One channel per line"
        )
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            channels_to_scrape = [ch.strip() for ch in content.split('\n') if ch.strip()]
    
    elif input_method == "Use Preset":
        if 'preset_channels' in st.session_state:
            channels_to_scrape = st.session_state.preset_channels
            st.info(f"Using preset: {', '.join(channels_to_scrape)}")
        else:
            st.warning("No preset selected. Please choose a preset above.")
    
    if channels_to_scrape:
        st.success(f"📋 Found {len(channels_to_scrape)} channel(s) to scrape")
        
        # Display channels
        with st.expander("📋 Channels to scrape"):
            for i, channel in enumerate(channels_to_scrape, 1):
                st.write(f"{i}. {channel}")
        
        # Scraping controls
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.button("🚀 Start Scraping", type="primary"):
                scrape_channels(channels_to_scrape, batch_size, days_back, max_videos)
        
        with col2:
            if st.button("📊 Show Results"):
                display_results()
        
        with col3:
            if st.button("🗑️ Clear Data"):
                clear_data()
    
    # Display storage summary
    display_storage_summary()

def scrape_channels(channels, batch_size, days_back, max_videos):
    """Scrape multiple channels with progress tracking"""
    if not st.session_state.scraper:
        st.error("❌ Scraper not initialized")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    results_container = st.container()
    
    total_channels = len(channels)
    all_scraped_data = []
    
    for i, channel in enumerate(channels):
        try:
            status_text.text(f"🔍 Processing channel {i+1}/{total_channels}: {channel}")
            progress_bar.progress((i) / total_channels)
            
            # Extract channel ID if needed
            channel_id = extract_channel_id(channel)
            if not channel_id:
                # Try to get channel ID from channel name
                channel_id = st.session_state.scraper.get_channel_id_from_name(channel)
            
            if not channel_id:
                st.error(f"❌ Could not find channel: {channel}")
                continue
            
            # Scrape channel data
            channel_data = st.session_state.scraper.scrape_channel(
                channel_id, 
                batch_size=batch_size,
                days_back=days_back,
                max_videos=max_videos
            )
            
            if channel_data:
                # Prepare batch info
                batch_info = {
                    'batch_size': batch_size,
                    'days_back': days_back,
                    'max_videos': max_videos,
                    'scrape_method': 'unlimited' if max_videos is None else 'limited'
                }
                
                # Store data with batch info
                st.session_state.storage.store_channel_data(channel, channel_data, batch_info)
                all_scraped_data.extend(channel_data)
                
                with results_container:
                    if max_videos is None:
                        st.success(f"✅ Successfully scraped ALL {len(channel_data)} videos from {channel}")
                    else:
                        st.success(f"✅ Successfully scraped {len(channel_data)} videos from {channel}")
            else:
                st.warning(f"⚠️ No data found for channel: {channel}")
                
        except Exception as e:
            st.error(f"❌ Error scraping {channel}: {str(e)}")
    
    # Final progress update
    progress_bar.progress(1.0)
    status_text.text(f"✅ Completed scraping {total_channels} channels")
    
    # Update session state
    st.session_state.scraped_data = all_scraped_data
    
    if all_scraped_data:
        if max_videos is None:
            st.success(f"🎉 Successfully scraped {len(all_scraped_data)} total videos with NO LIMIT!")
        else:
            st.success(f"🎉 Successfully scraped {len(all_scraped_data)} total videos!")
        display_results()

def display_results():
    """Display scraped results with visualizations"""
    if not st.session_state.scraped_data:
        st.warning("⚠️ No data to display. Please scrape some channels first.")
        return
    
    st.header("📊 Scraping Results")
    
    # Convert to DataFrame
    df = pd.DataFrame(st.session_state.scraped_data)
    
    # Summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Videos", len(df))
    
    with col2:
        total_views = df['view_count'].astype(float).sum()
        st.metric("Total Views", format_number(total_views))
    
    with col3:
        avg_views = df['view_count'].astype(float).mean()
        st.metric("Avg Views", format_number(avg_views))
    
    with col4:
        unique_channels = df['channel_name'].nunique()
        st.metric("Channels", unique_channels)
    
    # Data table
    st.subheader("📋 Video Data")
    
    # Add filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_channels = st.multiselect(
            "Filter by channel:",
            options=df['channel_name'].unique(),
            default=df['channel_name'].unique()
        )
    
    with col2:
        min_views = st.number_input(
            "Minimum views:",
            min_value=0,
            value=0,
            step=1000
        )
    
    # Apply filters
    filtered_df = df[
        (df['channel_name'].isin(selected_channels)) &
        (df['view_count'].astype(float) >= min_views)
    ]
    
    # Display filtered data
    st.dataframe(
        filtered_df[['title', 'channel_name', 'published_at', 'view_count', 'like_count', 'comment_count']],
        use_container_width=True
    )
    
    # Visualizations
    st.subheader("📈 Data Visualizations")
    
    if len(filtered_df) > 0:
        # Views by channel
        fig1 = px.bar(
            filtered_df.groupby('channel_name')['view_count'].sum().reset_index(),
            x='channel_name',
            y='view_count',
            title='Total Views by Channel'
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Views over time
        filtered_df['published_date'] = pd.to_datetime(filtered_df['published_at']).dt.date
        daily_views = filtered_df.groupby('published_date')['view_count'].sum().reset_index()
        
        fig2 = px.line(
            daily_views,
            x='published_date',
            y='view_count',
            title='Views Over Time'
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # Top videos
        top_videos = filtered_df.nlargest(10, 'view_count')
        fig3 = px.bar(
            top_videos,
            x='view_count',
            y='title',
            orientation='h',
            title='Top 10 Videos by Views'
        )
        fig3.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig3, use_container_width=True)

def display_storage_summary():
    """Display storage summary"""
    st.sidebar.header("💾 Storage Summary")
    
    # JSON files summary
    json_files = st.session_state.storage.get_json_files()
    st.sidebar.write(f"📁 JSON Files: {len(json_files)}")
    
    # In-memory storage summary
    memory_data = st.session_state.storage.get_all_data()
    total_videos = sum(len(data) for data in memory_data.values())
    st.sidebar.write(f"🧠 Memory Storage: {len(memory_data)} channels, {total_videos} videos")
    
    # Export options
    if st.sidebar.button("📥 Export All Data"):
        export_data()

def export_data():
    """Export all scraped data"""
    all_data = st.session_state.storage.get_all_data()
    
    if not all_data:
        st.warning("⚠️ No data to export")
        return
    
    # Create comprehensive export
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'total_channels': len(all_data),
        'total_videos': sum(len(videos) for videos in all_data.values()),
        'channels': all_data
    }
    
    # Save to JSON
    filename = f"youtube_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    st.session_state.storage.save_to_json(export_data, filename)
    
    st.success(f"📥 Data exported to {filename}")

def clear_data():
    """Clear all scraped data"""
    st.session_state.scraped_data = []
    st.session_state.storage.clear_all_data()
    st.success("🗑️ All data cleared")
    st.rerun()

if __name__ == "__main__":
    main()
