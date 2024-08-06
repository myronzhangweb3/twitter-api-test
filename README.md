# Twitter API Test(By RapidAPI)

Get a list of twitter followers, and filter users who retweeted a given tweet based on a keyword. Export all data to the output folder

## Usage

### Get API KEY

https://rapidapi.com/omarmhaimdat/api/twitter154

### Set environment variables

```shell
cp .env.example .env
```

### Install Package

```shell
pip install -r requirements.txt
```

### Run the code

The results are output to the output folder

#### Get followers
    
```shell
python3 followers.py
# Example of document content：1454078874644467718, {'user_id': '1454078874644467718', 'username': 'myronzhangweb3', 'timestamp': '2021-10-29 21:33:30'}
```

#### Search retweets
    
```shell
python3 search_retweets.py
# Example of document content：1820645081654956121: {'user_id': '1454078874644467718', 'username': 'myronzhangweb3', 'timestamp': '2024-08-06 10:16:28', 'tweet_id': '1820645081654956121'}
```