#sentiment_analysis.py
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from preprocess import preprocess_text  # Importing the preprocessing function

nltk.download('vader_lexicon')

# Initialize VADER Sentiment Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_news(articles):
    """
    Performs sentiment analysis on news articles using VADER.
    Returns a list of articles with sentiment scores.
    """
    analyzed_articles = []

    for article in articles:
        cleaned_text = preprocess_text(article["title"])  # Preprocess title text
        sentiment_score = sia.polarity_scores(cleaned_text)["compound"]
        sentiment = "Positive" if sentiment_score > 0.05 else "Negative" if sentiment_score < -0.05 else "Neutral"

        analyzed_articles.append({
            "title": article["title"],
            "link": article["link"],
            "source": article["source"],
            "published": article["published"],
            "sentiment": sentiment,
            "score": sentiment_score
        })

    return analyzed_articles
