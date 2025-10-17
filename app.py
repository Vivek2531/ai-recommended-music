import streamlit as st
from googleapiclient.discovery import build
from ai_helper import get_music_genre

# Simple page setup
st.title("🎧 Music Mood Mixer")

# Get keys
aws_key = st.secrets["aws"]["access_key_id"]
aws_secret = st.secrets["aws"]["secret_access_key"]
aws_region = st.secrets["aws"]["region"]
youtube_key = st.secrets["youtube"]["api_key"]

# Search bar
mood = st.text_input("🎵 How are you feeling?", placeholder="happy, sad, 😊, 😢, relaxed...")

if mood:
    # Get genre from AI
    genre = get_music_genre(mood, aws_key, aws_secret, aws_region)
    st.success(f"Perfect for you: **{genre}**")
    
    # Search YouTube
    try:
        youtube = build("youtube", "v3", developerKey=youtube_key)
        results = youtube.search().list(
            part="snippet",
            q=f"{genre} music",
            type="video",
            maxResults=5
        ).execute()
        
        # Show songs
        for song in results["items"]:
            title = song["snippet"]["title"]
            video_id = song["id"]["videoId"]
            st.markdown(f"🎵 **{title}**")
            st.video(f"https://www.youtube.com/watch?v={video_id}")
            
    except:
        st.error("⚠️ Can't load music right now. Check your YouTube API key.")
