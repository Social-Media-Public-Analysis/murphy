import dask
import dask.bag as db
import json
import bz2
from typing import List
from glob import glob
from os import path


class DataLoading:

    @staticmethod
    def get_files_list(pathname: str, recursive: bool = False, suffix: str = '*.json*') -> List[str]:
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

        files_list = glob(pathname, recursive=recursive)

        if not files_list:
            raise ValueError('File path given does not return any files')

        return files_list

    @staticmethod
    def read_compressed_bz2_json_file(file_path: str) -> List[dict]:
        """
        Read a compressed bz2 json file. Best used when you have a list of json files
        :param file_path: path of the file that needs to be read
        :return: List of json like dictionaries that contain information on tweets
        """
        if 'json.bz2' not in file_path:
            raise ValueError('File Passed is not json.bz2 file')
        file = bz2.open(file_path)
        data = file.read().decode("utf-8").split('\n')[:-1]
        return [json.loads(tweet) for tweet in data]

    @staticmethod
    def read_compressed_bz2_json_text(file_contents: str):
        """
        create json data from compressed bz2 text.
        Note: dask.bags.read_text might already uncompress this data, hence compression has been skipped here
        :param file_contents: text that is in a json/dict string
        :return: List of json like dictionaries that contain information on tweets
        """
        data = json.loads(file_contents)
        return data

    @staticmethod
    def get_twitter_data_as_bags(file_find_expression='../../data/*.json.bz2') -> dask.bag:
        """
        function to get twitter data as dask bags based on the given directory
        :param file_find_expression: unix like expression for finding the relevant files
        :return: dask bag that contains information on the tweets
        """
        bags = db.read_text(file_find_expression).map(DataLoading.read_compressed_bz2_json_text)
        return bags


if __name__ == '__main__':
    pass
