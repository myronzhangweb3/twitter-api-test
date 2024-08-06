import os
import time
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

TWITTER_SEARCH_QUERY = os.getenv('TWITTER_SEARCH_QUERY')
API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
TWITTER_SEARCH_RETWEETS_ID = os.getenv('TWITTER_SEARCH_RETWEETS_ID')
QUERY_LIMIT = 50

headers = {
    'x-rapidapi-key': API_KEY,
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Accept': '*/*',
    'Host': 'twitter154.p.rapidapi.com',
    'Connection': 'keep-alive'
}


def format_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def fetch_tweets(_query, continuation_token=None):
    params = {
        'query': _query,
        'limit': QUERY_LIMIT
    }
    print(f"request search tweets. Params: {params}")

    if continuation_token:
        params['continuation_token'] = continuation_token

    response = requests.get(BASE_URL + "/search/search", headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error fetching tweets: {response.status_code}")
        return None

    return response.json()


def process_tweets(tweets):
    result = {}
    last_tweet_id = None
    for tweet in tweets:
        if tweet.get('quoted_status_id') == TWITTER_SEARCH_RETWEETS_ID:
            tweet_id = tweet.get("tweet_id")
            timestamp = tweet.get('timestamp')
            user_id = tweet['user']['user_id']
            username = tweet['user']['username']
            result[tweet_id] = {
                'user_id': user_id,
                'username': username,
                'timestamp': timestamp,
                'tweet_id': tweet_id
            }
            last_tweet_id = tweet_id
            print(f"Processed tweet from {username} (ID: {user_id}) at {format_time(timestamp)}")

    return result, last_tweet_id


def write_search_result_to_file(result):
    with open('output/search_retweets.txt', 'w') as f:
        for user_id, data in result.items():
            f.write(f"{user_id}: {data}\n")


def main():
    retweets_result = {}
    while True:
        continuation_token = None
        while True:
            # Get Tweets, The results are sorted in reverse chronological order
            result = fetch_tweets(TWITTER_SEARCH_QUERY, continuation_token)
            if result and 'results' in result:
                tweets_infos, last_tweet_id = process_tweets(result['results'])

                # If there are no more tweets or the most current tweet has already been processed, stop the
                stop = (len(result) < QUERY_LIMIT or
                        (last_tweet_id is not None and last_tweet_id in retweets_result))

                # Processing tweets_infos
                for tweet_id, tweets_info in tweets_infos.items():
                    if tweet_id not in retweets_result:
                        retweets_result[tweet_id] = tweets_info

                if stop:
                    print("No more continuation tokens, stopping.")
                    break

                continuation_token = result.get('continuation_token')

                time.sleep(2)

        # Save results
        print(f"search result count: {len(retweets_result)}")
        if retweets_result:
            write_search_result_to_file(retweets_result)
        time.sleep(10)


if __name__ == "__main__":
    main()
