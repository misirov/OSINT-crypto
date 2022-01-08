import os
import tweepy
import twint
from dotenv import load_dotenv
import database as db

load_dotenv()
bearer = os.getenv("BEARER")
client = tweepy.Client(bearer_token=bearer)

'''
scrape list of users' friends using twitter api calls.
'''
def get_users_friends(username):
    '''
    need to first get the id of the user, since client.get_users_following() only accepts id as param.
    '''
    user = client.get_user(username=username)
    id = user[0].id

    '''
    request users' friends and update database. For now, only users with <1000 friends.
    '''
    friends_request = client.get_users_following(id=id, max_results=1000)
    friends = list(map(str, friends_request[0]))
    db.update_friends(str(user[0]), str(friends))


'''
simply scrape for amount of friends, without using (wasting) twitter api calls.
patched twint/user.py for this one.
'''
def get_users_friends_amount(username):
    c = twint.Config()
    c.Username = username
    c.Store_object = True

    twint.run.Lookup(c)

    user = twint.output.users_list[0]
    del twint.output.users_list[0]  #  free this ram for next call
    return user.following



