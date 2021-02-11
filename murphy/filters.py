"""
author: v2thegreat (v2thegreat@gmail.com)

Package to filter out irrelevant rows that might not be wanted for processing

TODO:
    - This package is written with the hopes to better understand what problems processing such a dataset would be
    encountered, and it is hence written with the understanding that this and other scripts will be refactored
    - Add tests
"""


from dask.dataframe import DataFrame as dask_Dataframe
from emoji import UNICODE_EMOJI
import emoji
import re


class Filter:
    _demojifier_regex = r':.+?:'
    _retweet_regex = r'RT @(.+?):'
    _truncated_string = '…'

    def __init__(self,
                 remove_emoji: bool = True,
                 remove_retweets: bool = False,
                 remove_truncated_tweets: bool = False):
        """
        Create Filter object that can filter out unneeded rows
        """
        self.remove_emoji_flag = remove_emoji
        self.remove_retweets_flag = remove_retweets
        self.remove_truncated_tweets_flags = remove_truncated_tweets

    @staticmethod
    def _is_emoji(string):
        count = 0
        for emoji_string in UNICODE_EMOJI:
            count += string.count(emoji_string)
            if count != 0:
                return True
        else:
            return False

    @staticmethod
    def _remove_emojis(string: str):
        string = emoji.demojize(string)
        return re.sub(Filter._demojifier_regex, '', string)

    @staticmethod
    def _remove_retweet(string: str):
        return re.sub(Filter._retweet_regex, '', string)

    @staticmethod
    def filter_emoji(twitter_dataframe: dask_Dataframe):
        twitter_dataframe['text'] = twitter_dataframe['text'].apply(Filter._remove_emojis, meta=str)
        return twitter_dataframe

    @staticmethod
    def filter_retweet_text(twitter_dataframe: dask_Dataframe):
        twitter_dataframe['text'] = twitter_dataframe['text'].apply(Filter._remove_retweet,
                                                                    meta=str)
        return twitter_dataframe

    @staticmethod
    def remove_truncated_tweets(tweet_dataframe: dask_Dataframe):
        tweet_dataframe['is_not_truncated_tweet'] = tweet_dataframe['text'].apply(
            lambda x: x[-1] != Filter._truncated_string, meta=bool)
        tweet_dataframe = tweet_dataframe[tweet_dataframe['is_not_truncated_tweet']]
        del tweet_dataframe['is_not_truncated_tweet']
        tweet_dataframe = tweet_dataframe.reset_index()
        del tweet_dataframe['index']
        return tweet_dataframe

    @staticmethod
    def mark_truncated_tweets(tweet_dataframe: dask_Dataframe):
        tweet_dataframe['is_truncated_tweet'] = tweet_dataframe['text'].apply(
            lambda x: x[-1] != Filter._truncated_string, meta=bool
        )
        return tweet_dataframe

    def run_filters(self, twitter_dataframe: dask_Dataframe):
        if self.remove_retweets_flag:
            twitter_dataframe = self.filter_retweet_text(twitter_dataframe)
        if self.remove_emoji_flag:
            twitter_dataframe = self.filter_emoji(twitter_dataframe)
        if self.remove_truncated_tweets_flags:
            twitter_dataframe = self.remove_truncated_tweets(twitter_dataframe)
        return twitter_dataframe


if __name__ == "__main__":
    pass
