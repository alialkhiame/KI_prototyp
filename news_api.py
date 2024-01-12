import requests
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk import download

# Download the VADER lexicon for sentiment analysis
download('vader_lexicon')

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()


# Function to fetch news articles from the API
def fetch_news(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Function to analyze articles for sentiment and update sumValue
def analyze_articles(articles, sumValue):
    i = 0
    for article in articles:
        title = article['title']
        time = article['publishedAt']
        content = article['content']
        sentiment_score = sia.polarity_scores(content)
        sumValue += sentiment_score['compound']

        # Interpret sentiment based on the compound score
        if sentiment_score['compound'] >= 0.1:
            sentiment = "Positive"
        elif sentiment_score['compound'] <= -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"

        #print(f"{i} posted on {time}")
        #print(f"Title: {title}\nSentiment: {sentiment}\nScore: {sentiment_score['compound']}\n")
        i += 1

    return sumValue  # Return the updated sumValue


def get_sum():
    return sumValue


# Change the following values
# (only the numbers for the dates otherwise the fetch won't work)
timeFrame = 'from=2023-12-20&to=2023-01-01'
topics = 'war'

# Specify the API endpoint URL
api_url = f"https://newsapi.org/v2/everything?q={topics}&{timeFrame}&apiKey=eb1e592755f345f6aeaac5379de92542"
articles = fetch_news(api_url)

# value that determines the "chance" of war
# the lower the number is, the worse the situation
# the higher the number is, the better the situation
# 0 is neutral
sumValue = 0

if articles:
    sumValue = analyze_articles(articles['articles'], sumValue)
    overall_sentiment = "Positive" if sumValue >= 0 else "Negative"
  #  print(f"Overall Sentiment: {overall_sentiment}, Overall Score: {sumValue}")
else:
    print("Failed to fetch news articles")

print(get_sum())
