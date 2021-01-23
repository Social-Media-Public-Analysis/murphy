import bz2
from pathlib import Path
import json
from glob import glob
from os import path
from typing import List, Union

import dask.bag as db
import dask.dataframe as dd

from murpheus.filters import Filter


class DataLoader:
    __instance__ = None

    def __init__(self,
                 file_find_expression: Union[str, Path, List[Path]],
                 remove_emoji: bool = True,
                 remove_retweets: bool = True,
                 remove_truncated_tweets: bool = True,
                 add_usernames: bool = True
                 ):

        self.filter = Filter(remove_emoji, remove_retweets, remove_truncated_tweets)
        self.file_find_expression = file_find_expression
        self.file_list = self._get_files_list(self.file_find_expression)
        self.twitter_dataframe = self._get_twitter_data_as_dataframes()
        self.twitter_bags = self._get_twitter_data_as_bags()
        self.twitter_dataframe = self.filter.run_filters(self.twitter_dataframe)

        if add_usernames:
            self._add_usernames()

    @staticmethod
    def _get_files_list(pathname: Union[str, Path], recursive: bool = False,
                        suffix: str = '*.json*') -> List[str]:
        """
        function to get files from the given pathname.
        Searches in the directory when pathname leads to a directory with the option for adding a custom suffix

        If pathname given is a directory, searches in the directory

        :param pathname: pathname from
        :param recursive: Flag for searching recursively
        :param suffix: suffix to search for files when a pathname leads to a directory is given
        :raises ValueError: When no files are found based on the pathname
        :return:
        """

        if path.isdir(pathname):
            pathname = path.join(pathname, f'{suffix}')

        pathname = str(pathname)

        files_list = glob(pathname, recursive=recursive)

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
        create json data from compressed bz2 text.
        Note: dask.bags.read_text might already uncompress this data, hence compression has been skipped here
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
        function to get twitter data as dask bags based on the given directory
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
        self.twitter_dataframe['user_names'] = self.twitter_dataframe['user'].apply(lambda x: x['screen_name'],
                                                                                    meta=str)

    # def group_user_tweets(self):
    #     # TODO: add functionality in batch processing to make this process easier and more memory efficient
    #     if 'user_names' not in self.twitter_dataframe.columns:
    #         self._add_usernames()
    #     return self.twitter_dataframe.groupby('user_names').apply(lambda x: list(x['text']), meta=list).to_frame()


if __name__ == '__main__':
    pass
