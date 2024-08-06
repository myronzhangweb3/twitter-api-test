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
```

#### Search retweets
    
```shell
python3 search_retweets.py
```