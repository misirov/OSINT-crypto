import os
import tweepy
from dotenv import load_dotenv

#  find changes in new followings with simple scraping
#  must scrape all new followings of important accounts
#  must note similarities in new followings

load_dotenv()
bearer = os.getenv("BEARER")

client = tweepy.Client(bearer_token=bearer)

user_id = 1092107522100600837  # id of @JordiJansen101

#  https://docs.tweepy.org/en/stable/client.html#users
#  can pass friends_request.token
friends_request = client.get_users_following(id=user_id, max_results=1000)

for i in friends_request[0]:
    print(i)
