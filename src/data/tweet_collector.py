import ast
# import jgraph
import csv
import operator
import os

import numpy as np
import pandas as pd
import tweepy
from dotenv import load_dotenv

load_dotenv('../../.env')


class TweetGrabber:

    def __init__(self, twitter_api_key, twitter_api_key_secret, twitter_access_token, twitter_access_token_secret):
        self.tweepy = tweepy
        auth = tweepy.OAuthHandler(twitter_api_key, twitter_api_key_secret)
        auth.set_access_token(twitter_access_token, twitter_access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # @staticmethod
    # def strip_non_ascii(string):
    #     """ Returns the string without non ASCII characters"""
    #     stripped = (c for c in string if 0 < ord(c) < 127)
    #     return ''.join(stripped)

    def keyword_search(self, keyword, csv_prefix):
        api_results = self.api.search(q=keyword, rpp=1000, show_user=True, tweet_mode='extended')

        with open(f'../../data/raw/tweet_collector/{csv_prefix}.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'follower_count',
                          'retweet_count', 'user_mentions']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in api_results:
                text = tweet.full_text.encode('utf-8')
                date = tweet.created_at.strftime('%m/%d/%Y')
                writer.writerow({
                    'tweet_id': tweet.id_str,
                    'tweet_text': text,
                    'date': date,
                    'user_id': tweet.user.id_str,
                    'follower_count': tweet.user.followers_count,
                    'retweet_count': tweet.retweet_count,
                    'user_mentions': tweet.entities['user_mentions']
                })

    def user_search(self, user, csv_prefix):
        api_results = self.tweepy.Cursor(self.api.user_timeline, id=user, tweet_mode='extended').items()

        with open(f'../../data/raw/tweet_collector/{csv_prefix}.csv', 'w', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['tweet_id', 'tweet_text', 'date', 'user_id', 'user_mentions', 'retweet_count']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()

            for tweet in api_results:
                text = tweet.full_text.encode('utf-8')
                date = tweet.created_at.strftime('%m/%d/%Y')
                writer.writerow({
                    'tweet_id': tweet.id_str,
                    'tweet_text': text,
                    'date': date,
                    'user_id': tweet.user.id_str,
                    'user_mentions': tweet.entities['user_mentions'],
                    'retweet_count': tweet.retweet_count
                })


class RetweetParser:

    def __init__(self, data, user):
        self.user = user

        edge_list = []

        for idx, row in data.iterrows():
            if len(row[4]) > 5:
                user_account = user
                weight = np.log(row[5] + 1)
                for idx_1, item in enumerate(ast.literal_eval(row[4])):
                    edge_list.append((user_account, item['screen_name'], weight))

                    for idx_2 in range(idx_1 + 1, len(ast.literal_eval(row[4]))):
                        name_a = ast.literal_eval(row[4])[idx_1]['screen_name']
                        name_b = ast.literal_eval(row[4])[idx_2]['screen_name']

                        edge_list.append((name_a, name_b, weight))

        import csv
        with open(f'{self.user}.csv', 'w', newline='') as csvfile:
            fieldnames = ['user_a', 'user_b', 'log_retweet']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in edge_list:
                writer.writerow({
                    'user_a': row[0],
                    'user_b': row[1],
                    'log_retweet': row[2]
                })


class TweetGraph:

    def __init__(self, edge_list):
        data = pd.read_csv(edge_list).to_records(index=False)
        self.graph = igraph.Graph.TupleList(data, weights=True, directed=False)

    def e_centrality(self):
        vectors = self.graph.eigenvector_centrality()
        e = {name: cen for cen, name in zip([v for v in vectors], self.graph.vs['name'])}
        return sorted(e.items(), key=operator.itemgetter(1), reverse=True)


t = TweetGrabber(
    twitter_api_key=os.getenv('TWITTER_API_KEY'),
    twitter_api_key_secret=os.getenv('TWITTER_API_KEY_SECRET'),
    twitter_access_token=os.getenv('TWITTER_API_ACCESS_TOKEN'),
    twitter_access_token_secret=os.getenv('TWITTER_API_ACCESS_TOKEN_SECRET'))
t.user_search(user='One4AllGiftUK', csv_prefix='One4All_tweets')
t.user_search(user='One4AllGiftUK', csv_prefix='One4All_tweets')

r = RetweetParser(, '')
#
# m_graph = MyGraph(edge_list='.csv')
# m_graph.e_centrality()
