"""
author: v2thegreat (v2thegreat@gmail.com)

Package to process tweets from the data_loading in batches to reduce the workload on the scheduler
by applying various functions in batches

"""

import bz2
from pathlib import Path
import json
from glob import glob
from os import path
from typing import List, Union
import dask.bag as db
import dask.dataframe as dd
from murphy.filters import Filter
from murphy.nlp_tools import NLPTools


class DataLoader:
    __instance__ = None

    def __init__(self,
                 file_find_expression: Union[str, Path, List[Path]],
                 remove_emoji: bool = True,
                 remove_retweets_symbols: bool = True,
                 remove_truncated_tweets: bool = True,
                 add_usernames: bool = True,
                 tokenize: bool = True,
                 filter_stopwords: bool = True,
                 lemmatize: bool = True,
                 language: str = 'english'
                 ):
        """

        This is where you can specify how you want to configure the twitter dataset before you start processing it.

        :param file_find_expression: unix-like path that is used for listing out all of the files that we need

        :param remove_emoji: flag for removing emojis from all of the twitter text

        :param remove_retweets_symbols: flag for removing retweet strings from all of the twitter text (`RT @<retweet_username>:`)

        :param remove_truncated_tweets: flag for removing all tweets that are truncated, as not all information can be
                                        found in them

        :param add_usernames: flag for adding in the user names from who tweeted as a separate column instead of parsing
                              it from the `user` column
        
        :param tokenize: tokenize tweets to make them easier to process
        
        :param filter_stopwords: remove stopwords from the tweets to make them easier to process
        
        :param lemmatize: lemmatize text to make it easier to process
        
        :param language: select the language that you want to work with
        """

        self.filter = Filter(
            remove_emoji = remove_emoji,
            remove_retweets = remove_retweets_symbols,
            remove_truncated_tweets = remove_truncated_tweets
        )

        self.nlp_tools = NLPTools(
            tokenize = tokenize,
            filter_stopwords = filter_stopwords,
            lemmatize = lemmatize,
            language = language
        )

        self.file_find_expression = file_find_expression
        self.file_list = self.get_files_list(self.file_find_expression)
        self.twitter_dataframe = self._get_twitter_data_as_dataframes()
        self.twitter_bags = self._get_twitter_data_as_bags()
        self.twitter_dataframe = self.filter.run_filters(self.twitter_dataframe)
        self.twitter_dataframe = self.nlp_tools.run_tools(self.twitter_dataframe)

        if add_usernames:
            self._add_usernames()

    @staticmethod
    def get_files_list(pathname: Union[str, Path], recursive: bool = False,
                       suffix: str = '*.json*') -> List[str]:
        """
        Function to get files from the given pathname.

        Searches in the directory when pathname leads to a directory with the option for adding a custom suffix

        If pathname given is a directory, searches in the directory

        :param pathname: pathname from where we can get the files

        :param recursive: Flag for searching recursively

        :param suffix: suffix to search for files when a pathname leads to a directory is given

        :raises ValueError: When no files are found based on the pathname

        :return:

        """

        if path.isdir(pathname):
            pathname = path.join(pathname, f'{suffix}')

        pathname = str(pathname)

        files_list = glob(pathname, recursive = recursive)

        if not files_list:
            raise ValueError('File path given does not return any files')

        return files_list

    @staticmethod
    def _read_compressed_bz2_json_file(file_path: Union[str, Path]) -> List[dict]:
        """
        Read a compressed bz2 json file. Best used when you have a list of json files

        :param file_path: path of the file that needs to be read

        :return: List of json like dictionaries that contain information on tweets

        """
        if 'json.bz2' not in str(file_path):
            raise ValueError('File Passed is not json.bz2 file')
        file = bz2.open(file_path)
        data = file.read().decode("utf-8").split('\n')[:-1]
        return [json.loads(tweet) for tweet in data]

    @staticmethod
    def _read_compressed_bz2_json_text(file_contents: Union[str, Path]):
        """
        Create json data from compressed bz2 text.
        **Note**: dask.bags.read_text might already uncompress this data, hence compression has been skipped here

        :param file_contents: text that is in a json/dict string

        :return: List of json like dictionaries that contain information on tweets

        """
        data = json.loads(file_contents)
        return data

    def _get_twitter_data_as_dataframes(self, remove_deleted_tweets: bool = True) -> dd.DataFrame:
        """
        Function to get twitter data as dask bags based on the given directory

        :param remove_deleted_tweets: Filter out removed tweets?
                Don't turn this off if you want something working right out of the box.

        :return: dask dataframe that contains information on the tweets
        """
        bags = db.read_text(self.file_find_expression).map(DataLoader._read_compressed_bz2_json_text)

        if remove_deleted_tweets:
            bags = DataLoader._remove_deleted_tweets(bags)

        return bags.to_dataframe()

    def _get_twitter_data_as_bags(self, remove_deleted_tweets: bool = True) -> db.Bag:
        """
        Function to get twitter data as dask bags based on the given directory

        :param remove_deleted_tweets: Filter out removed tweets?
                                Don't turn this off if you want something working right out of the box.

        :return: dask bag that contains information on the tweets

        """
        bags = db.read_text(self.file_find_expression).map(DataLoader._read_compressed_bz2_json_text)
        if remove_deleted_tweets:
            bags = DataLoader._remove_deleted_tweets(bags)
        return bags

    @staticmethod
    def _get_twitter_data_from_file_list(file_lst: List,
                                         remove_deleted_tweets: bool = True) -> db.Bag:
        """
        Function to get twitter data from the file list

        :param file_lst: list of files where we have all of our twitter data

        :param remove_deleted_tweets: ensure that tweets that were deleted are removed from our dataset

        :return: dask bag that has all of the tweets ready for processing

        """
        bags = db.read_text(file_lst).map(DataLoader._read_compressed_bz2_json_text)
        if remove_deleted_tweets:
            bags = DataLoader._remove_deleted_tweets(bags)
        return bags

    @staticmethod
    def _remove_deleted_tweets(data: db.Bag) -> db.Bag:
        """
        Function to remove unneeded tweets

        Deleted tweets don't include various parameters, including the `lang` parameter

        :param data: dask bags that contain the tweets

        :return: returns the items that haven't been deleted
        """
        return data.filter(lambda x: 'lang' in x)

    def _add_usernames(self):
        """
        Function to add usernames directly into the twitter_dataframe instead of using the user
        json file
        :return:

        """
        self.twitter_dataframe['user_names'] = self.twitter_dataframe['user'].apply(
            lambda x: x['screen_name'],
            meta = str)
        self.twitter_dataframe['user_names'] = self.twitter_dataframe['user'].apply(lambda x: x['screen_name'],
                                                                                    meta=str)

    # def group_user_tweets(self):
    #     # TODO: add functionality in batch processing to make this process easier and more memory efficient
    #     if 'user_names' not in self.twitter_dataframe.columns:
    #         self._add_usernames()
    #     return self.twitter_dataframe.groupby('user_names').apply(lambda x: list(x['text']), meta=list).to_frame()


if __name__ == '__main__':
    pass
