from fastapi import FastAPI, Query
from google_trends import get_trending_keywords
from youtube_trends import get_youtube_trending_videos
import openai
import os
from dotenv import load_dotenv

# ✅ Load API Keys
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# ✅ Debug: Check API Key (Masked for Security)
if not OPENAI_API_KEY:
    raise ValueError("❌ OpenAI API Key is missing! Check your .env file.")

app = FastAPI()

@app.get("/generate_ideas/")
def generate_video_ideas(
    topic: str = Query(..., title="Topic"),
    audience: str = Query("Beginners", title="Target Audience"),
    region: str = Query("US", title="Region")
):
    # ✅ Fetch Trending Keywords
    trending_keywords = get_trending_keywords(topic)
    if not trending_keywords:
        trending_keywords = ["No trending keywords found for this topic"]

    # ✅ Fetch Trending YouTube Videos
    trending_videos = get_youtube_trending_videos(topic, region)
    if not trending_videos:
        trending_videos = [{"title": "No trending videos found", "url": "#"}]

    # ✅ Generate YouTube Video Ideas using OpenAI
    prompt = f"""
    Generate 5 engaging YouTube video ideas on '{topic}' for '{audience}' that are currently trending.
    Consider these trending keywords: {', '.join(trending_keywords)}.
    Use insights from these trending YouTube videos: {', '.join([video['title'] for video in trending_videos])}.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        ideas = response.choices[0].message.content.strip()
    except Exception as e:
        ideas = f"❌ OpenAI API Error: {str(e)}"

    return {
        "trending_keywords": trending_keywords,
        "trending_videos": trending_videos,
        "ideas": ideas
    }
