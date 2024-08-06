import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
BASE_URL = os.getenv('BASE_URL')
USERNAME = os.getenv('USERNAME')
USER_ID = os.getenv('USER_ID')
QUERY_LIMIT = 100

HEADERS = {
    'x-rapidapi-key': API_KEY,
    'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
    'Accept': '*/*',
    'Host': 'twitter154.p.rapidapi.com',
    'Connection': 'keep-alive'
}


def get_user_id(username):
    print(f"request get_user_id api. username: {username}")
    url = f'{BASE_URL}/user/details?username={username}'
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data.get('user_id')


def get_followers(user_id, continuation_token=None):
    print(f"request followers api. user_id: {user_id}, limit: {QUERY_LIMIT}, continuation_token: {continuation_token}")
    if continuation_token:
        url = f'{BASE_URL}/user/followers/continuation?user_id={user_id}&limit={QUERY_LIMIT}&continuation_token={continuation_token}'
    else:
        url = f'{BASE_URL}/user/followers?user_id={user_id}&limit={QUERY_LIMIT}'
    response = requests.get(url, headers=HEADERS)
    return response.json()


def write_followers_to_file(followers):
    with open('output/follower.txt', 'a') as f:
        for user_id, username in followers.items():
            f.write(f"{user_id}, {username}\n")


def main():
    # query user_id
    user_id = USER_ID
    if not user_id:
        print("user_id not found, try to get it from username")
        user_id = get_user_id(USERNAME)
    print(f"check user_id: {user_id}")
    followers = {}

    # Loop through the list of followers
    while True:
        continuation_token = None
        while True:
            # Get followers, The results are sorted in reverse chronological order
            response = get_followers(user_id, continuation_token)
            followers_data = response.get('results', [])
            print(f"current query followers count: {len(followers_data)}")

            stop = (len(followers_data) < QUERY_LIMIT or
                    (followers_data[len(followers_data) - 1]['user_id'] is not None and
                     followers_data[len(followers_data) - 1]['user_id'] in followers))
            # Updating the list of followers
            for follower in followers_data:
                uid = follower['user_id']
                username = follower['username']
                if uid not in followers:
                    followers[uid] = username
                    print(f"new follower: {username}")

            if stop:
                print("finished")
                break

            continuation_token = response.get('continuation_token')

            time.sleep(3)

        # TODO You need to load all the followers every time you start up,
        #  writing them all at once should be changed to adding them dynamically.
        print(f"followers count: {len(followers)}")
        if followers:
            write_followers_to_file(followers)

        time.sleep(10)


if __name__ == "__main__":
    main()
