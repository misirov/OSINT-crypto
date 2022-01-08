import os
import pathlib
import time
import requests
import tweepy
from dotenv import load_dotenv
import database as db
from scraper import scrape

load_dotenv()
bearer = os.getenv("BEARER")
client = tweepy.Client(bearer_token=bearer)

'''
initialize database.
'''
if not os.path.isfile("koiosint.db"):
    db.create_table()

'''
import users from users.txt. The file should contain all users that we want to scrape, each on newline.
for now only users with less than 1000 friends (followings).
strip() is to remove newline character.
'''
with open('users.txt', 'r') as f:
    users = [line.strip() for line in f]


while True:
    for username in users:
        if len(db.query_user(username)) <= 0:
            scrape.get_users_friends(username)

        friends_cache = db.query_friends(username)
        friends_amount = scrape.get_users_friends_amount(username)

        if len(friends_cache) != friends_amount:
            old_list = friends_cache
            scrape.get_users_friends(username)
            new_list = db.query_friends(username)
            new_users = list(set(new_list) - set(old_list))
            removed_users = list(set(old_list) - set(new_list))

            print(username)
            print("new users: " + str(new_users))
            print(("removed users: " + str(removed_users)))

    print("SLEEPING")
    time.sleep(900)  # 15min
