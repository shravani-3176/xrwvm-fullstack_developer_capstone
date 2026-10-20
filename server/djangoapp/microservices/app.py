from flask import Flask, jsonify
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

try:
    sia = SentimentIntensityAnalyzer()
except Exception:
    nltk.download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()

app = Flask("Sentiment Analyzer")


@app.get('/')
def home():
    return "Welcome to the Sentiment Analyzer. Use /analyze/text to get the sentiment"


@app.get('/analyze/<input_txt>')
def analyze_sentiment(input_txt):
    scores = sia.polarity_scores(input_txt)
    print(scores)
    pos = float(scores['pos'])
    neg = float(scores['neg'])
    neu = float(scores['neu'])
    res = "positive"
    print("pos neg neu ", pos, neg, neu)
    if (neg > pos and neg > neu):
        res = "negative"
    elif (neu > neg and neu > pos):
        res = "neutral"
    return jsonify({"sentiment": res})


if __name__ == "__main__":
    app.run(port=5050, debug=True)
