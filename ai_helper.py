import boto3
import json
import os
from googleapiclient.discovery import build

def get_music_genre(mood, aws_key, aws_secret, aws_region):
    """Ask AI what music matches the mood"""
    bedrock = boto3.client(
        service_name='bedrock-runtime',
        region_name=aws_region,
        aws_access_key_id=aws_key,
        aws_secret_access_key=aws_secret
    )
    
    prompt = f"Someone feels: {mood}. Suggest a music genre in 2-4 words only."
    
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 30,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=body
    )
    
    result = json.loads(response['body'].read())
    return result['content'][0]['text'].strip()

def search_youtube_songs(genre, api_key):
    """Search YouTube for actual songs (not playlists or compilations)"""
    try:
        youtube = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
        
        # Search for actual songs - exclude playlists, compilations, mixes
        search_query = f"{genre} songs -playlist -mix -compilation -hours -album"
        
        results = youtube.search().list(
            part="snippet",
            q=search_query,
            type="video",
            videoCategoryId="10",  # Music category only
            videoDuration="medium",  # 4-20 minutes (typical song length)
            maxResults=10,  # Get more to filter better
            order="viewCount"  # Popular songs
        ).execute()
        
        videos = []
        for item in results.get("items", []):
            title = item['snippet']['title'].lower()
            
            # Skip if title contains playlist/mix/compilation keywords
            skip_keywords = ['playlist', 'mix', 'compilation', 'album', 'hours', 'best of', 'top 10']
            if any(keyword in title for keyword in skip_keywords):
                continue
            
            videos.append({
                'title': item['snippet']['title'],
                'id': item['id']['videoId'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url']
            })
            
            # Stop when we have 5 songs
            if len(videos) >= 5:
                break
        
        return videos
    except Exception as e:
        print(f"YouTube error: {e}")
        import traceback
        traceback.print_exc()
        return []
