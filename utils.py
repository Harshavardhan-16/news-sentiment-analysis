import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon")

def fetch_news(company_name):
    """
    Scrapes news articles related to the given company from Bing News.
    Returns a list of articles with title, summary, and URL.
    """
    search_url = f"https://www.bing.com/news/search?q={company_name}&form=QBNH"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch news"}

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []
    for news in soup.find_all("div", class_="news-card")[:10]: 
        title_tag = news.find("a")
        summary_tag = news.find("div", class_="snippet")

        if title_tag and summary_tag:
            articles.append({
                "title": title_tag.text.strip(),
                "summary": summary_tag.text.strip(),
                "url": title_tag["href"]
            })

    return articles

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def translate_to_hindi(text):
    try:
        return GoogleTranslator(source="auto", target="hi").translate(text)
    except Exception as e:
        print(f"Translation Error: {e}")
        return text 

def text_to_speech(text, lang, filename):
    try:
        if not text.strip():
            text = "No summary available." if lang == "en" else "कोई सारांश उपलब्ध नहीं है।"
        
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error generating TTS: {e}")
        return None
