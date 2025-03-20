import requests
import os
from dotenv import load_dotenv  # ✅ Ensure dotenv is loaded

# Load SerpAPI key
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def get_trending_keywords(topic="big data", region="US"):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_trends",
        "q": topic,  # 🔹 Ensure this query is passed
        "hl": "en",
        "date": "today 12-m",
        "tz": "420",
        "data_type": "RELATED_QUERIES",
        "api_key": SERPAPI_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    # ✅ Debug: Print the raw response
    print("\n✅ RAW RESPONSE:\n", data)

    if "related_queries" in data:
        # ✅ Extracting both 'rising' and 'top' trending queries
        keywords = [item["query"] for group in data["related_queries"].values() if group for item in group]
        return keywords
    else:
        return []

# Test the function
trending_keywords = get_trending_keywords("Artificial Intelligence")
print("\n🔥 Trending Keywords:", trending_keywords)








