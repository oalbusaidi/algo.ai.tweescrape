import re
import nltk
import demoji
import sqlite3
import pandas as pd
from googletrans import Translator
from deep_translator import GoogleTranslator
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

nltk.download('vader_lexicon')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')


def clean_text(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               "]+", flags=re.UNICODE
                               )
    # Remove emojis from the text
    text = re.sub(r'/', '', text)
    text = re.sub(r'\:', '', text)
    text = re.sub(r'\.', '', text)
    text = re.sub(r'\\', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'#\w+', '', text)
    text = re.sub(r'@\w+', '', text)
    text = emoji_pattern.sub(r'', text)
    text = re.sub(r'[a-zA-Z]', '', text)
    text = re.sub(r'http[s]?://\S+', '', text)
    text = demoji.replace(text, '')
    return text


def clean_tweets_dataframe():
    connection = sqlite3.connect('scraping_services/scraped_data.db')

    tweets_df = pd.read_sql_query("SELECT * from twitter_tweet", connection)
    user_df = pd.read_sql_query("SELECT * from twitter_user", connection)

    tweets_df['cleanedContent'] = tweets_df['rawContent'].apply(clean_text)
    tweets_df = tweets_df[tweets_df['lang'] != 'en']
    tweets_selected = tweets_df[[
        'userid', 'rawContent', 'replyCount', 'retweetCount',
        'likeCount', 'quoteCount', 'viewCount', 'date', 'cleanedContent'
    ]]
    tweets_no_duplicates = tweets_selected.drop_duplicates(
        keep='first', subset=['cleanedContent']
    )
    tweets_no_duplicates.loc[
        tweets_no_duplicates['viewCount'].isna(),
        'viewCount'
    ] = 0
    merge_with_location = pd.merge(
        tweets_no_duplicates,
        user_df[['userid', 'location']],
        on='userid',
        how='left'
    )
    return merge_with_location


def translate_to_en(text):
    translator = Translator()
    english_text = translator.translate(text, src='ar', dest='en').text
    return english_text


def get_sentiment_arabic(text):
    # Translate Arabic text to English
    english_text = translate_to_en(text)

    # Get the sentiment of the translated text
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(english_text)

    # Determine the sentiment based on the compound score
    if scores['compound'] >= 0.05:
        sentiment = 'Positive'
    elif scores['compound'] <= -0.05:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    return sentiment


def translate_text(text, source_lang='auto', target_lang='en'):
    try:
        translated = GoogleTranslator(
            source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        print(f"Error occurred during translation: {e}")
        return text


def get_top_influencers():
    connection = sqlite3.connect('scraping_services/scraped_data.db')
    tweets_no_duplicates = clean_tweets_dataframe()
    user_df = pd.read_sql_query("SELECT * from twitter_user", connection)
    tweet_data = tweets_no_duplicates[[
        'userid', 'cleanedContent', 'retweetCount', 'likeCount']].copy()

    # Calculate a score for each user based on retweets and likes
    tweet_data.loc[:, 'influenceScore'] = tweet_data['retweetCount'] + \
        tweet_data['likeCount']

    # Group by userID and sum the influence scores
    user_scores = tweet_data.groupby(
        'userid')['influenceScore'].sum().reset_index()

    # Sort users by influence score in descending order
    user_scores = user_scores.sort_values(by='influenceScore', ascending=False)

    # Display the top influencers
    top_influencers = user_scores.head(10)
    top_influencers_with_username = pd.merge(
        top_influencers, user_df, on='userid', how='left')
    return top_influencers_with_username


def get_top_locations():
    tweets_df = clean_tweets_dataframe()
    location_data = tweets_df[['location']].copy()

    # Drop rows with missing location data
    location_data = tweets_df.dropna()

    # Count the occurrences of each location
    location_counts = location_data['location'].value_counts()
    location_counts = location_counts.head(11)

    # Translate non-English location names to English
    translated_indexes = location_counts.index.map(translate_text)
    location_counts = pd.Series(
        location_counts.values, index=translated_indexes)

    return location_counts


def get_tweets_per_date():
    tweets_no_duplicates = clean_tweets_dataframe()
    tweets_no_duplicates['date'] = pd.to_datetime(tweets_no_duplicates['date'])

    # Extract relevant columns for temporal analysis
    temporal_data = tweets_no_duplicates[['date', 'retweetCount', 'likeCount']]

    # Group by date and sum the engagement metrics
    temporal_data = temporal_data.groupby('date').sum()
    print(type(temporal_data))
    return temporal_data


def get_top_users_replied_to():
    tweets_no_duplicates = clean_tweets_dataframe()
    connection = sqlite3.connect('scraping_services/scraped_data.db')
    user_df = pd.read_sql_query("SELECT * from twitter_user", connection)
    user_reply_counts = tweets_no_duplicates.groupby('userid')[
        'replyCount'].sum()

    # Sort users by the number of replies in descending order
    top_reply_users = user_reply_counts.sort_values(ascending=False).head(10)
    top_reply_users_with_names = pd.merge(
        top_reply_users, user_df, on='userid', how='left')

    return top_reply_users_with_names


def process_arabic_text(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    lemmatizer = WordNetLemmatizer()
    # Lemmatize the tokens using NLTK's WordNet lemmatizer
    stop_words = set(stopwords.words('arabic'))
    lemmatized_tokens = [lemmatizer.lemmatize(
        token) for token in tokens if token.isalpha() and token not in stop_words]

    return lemmatized_tokens


def process_arabic_text_tfidf(text):
    # Tokenize the text
    tokens = nltk.word_tokenize(text)

    lemmatizer = WordNetLemmatizer()
    # Lemmatize the tokens using NLTK's WordNet lemmatizer
    stop_words = set(stopwords.words('arabic'))
    lemmatized_tokens = [lemmatizer.lemmatize(
        token) for token in tokens if token.isalpha() and token not in stop_words]

    return ' '.join(lemmatized_tokens)


def get_most_common_words_with_counts_nltk():
    # Example Arabic text processing function

    tweets_no_duplicates = clean_tweets_dataframe()
    # Apply the processing function to each row of the 'cleanedContent' column
    tweets_no_duplicates['processed_tokens'] = tweets_no_duplicates['cleanedContent'].astype(
        str).apply(process_arabic_text)

    # Flatten the list of lists to get all lemmatized tokens
    all_lemmatized_tokens = [
        token for tokens in tweets_no_duplicates['processed_tokens'] for token in tokens]

    # Count the occurrences of each lemmatized token
    lemmatized_token_counts = Counter(all_lemmatized_tokens)

    # Get the most common lemmatized tokens and their frequencies
    top_tokens = [token for token,
                  count in lemmatized_token_counts.most_common(10)]
    token_counts = [count for token,
                    count in lemmatized_token_counts.most_common(10)]
    return pd.DataFrame({"topWord": top_tokens, "wordCount": token_counts})


def get_top_keywords(tfidf_matrix, feature_names, n=10):
    # Get the TF-IDF scores for each token
    tfidf_scores = tfidf_matrix.sum(axis=0).A1

    # Sort the tokens by TF-IDF scores in descending order
    sorted_indices = tfidf_scores.argsort()[::-1]

    # Get the top N keywords
    top_keywords = [(feature_names[i], tfidf_scores[i])
                    for i in sorted_indices[:n]]

    return top_keywords


def get_most_common_words_with_counts_tfidf():
    tweets_no_duplicates = clean_tweets_dataframe()
    # Apply the processing function to each row of the 'cleanedContent' column
    tweets_no_duplicates['processed_text'] = tweets_no_duplicates['cleanedContent'].astype(
        str).apply(process_arabic_text_tfidf)

    # Convert the lemmatized text data into a list
    lemmatized_text_list = tweets_no_duplicates['processed_text'].tolist()

    # Initialize TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the lemmatized text data
    tfidf_matrix = tfidf_vectorizer.fit_transform(lemmatized_text_list)

    # Get feature names
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Get the top keywords based on TF-IDF scores

    # Get the top keywords
    top_keywords = get_top_keywords(tfidf_matrix, feature_names)
    top_words = []
    top_words_count = []
    for keyword, score in top_keywords:
        top_words.append(keyword)
        top_words_count.append(score)

    return pd.DataFrame({'topWord': top_words, 'wordCount': top_words_count})


def get_sentiment_results():
    return {
        'positive': 1068,
        'neutral': 629,
        'negative':  1333,
    }

def get_topic_modelling():
    topics = [
        'اختار جسر ',
        'معالي وزير الاسكان يرعى تطوير مشروع استثمارية بقيمة مليون',
        'سوف يعلن  أسماء المستحقين لمدينة السكنية الإسكان الحكومية',
        'نتشارك في الانتفاع بأرض  من خلال نظام المزايدة.',
        'تعمل وزارة الاسكان  على تنمية مسقط العمرانية',
    ]

    return pd.DataFrame({'topic': topics})