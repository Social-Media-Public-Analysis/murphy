import unittest
from dask.bag import Bag
from murphy.data_loading import DataLoading
from tests import CommonTestSetup
from pathlib import Path


class DataLoadingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()

    def test_singleton(self):
        try:
            data_load_1 = DataLoading()
            data_load_2 = DataLoading()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)

    def test_get_files_list_in_data(self):
        """
        Note:
            function assumes that order doesn't matter
            If order matters, glob might have to be reconfigured
        """
        sample_files_list = set([(Path(x)) for x in DataLoading.get_files_list(self.data_path)])
        self.assertTrue(sample_files_list == {self.path_prefix / 'data/test_data/test_sample_files.json.bz2',
                                              self.path_prefix / 'data/test_data/test_sample_files_2.json.bz2'})

    def test_get_files_list_when_no_files_present(self):
        print(self.data_path)
        try:
            DataLoading.get_files_list('../../data/no-files.abcd')
            self.assertFalse(False)
        except ValueError:
            self.assertTrue(True)

    def test_get_files_list_when_directory(self):
        files_list = DataLoading.get_files_list(self.data_path, suffix='*.json.bz2')

        self.assertTrue(set(files_list) == {str(self.data_path / 'test_sample_files.json.bz2'),
                                            str(self.data_path / 'test_sample_files_2.json.bz2')})

    def test_read_compressed_bz2_json_file(self):
        data = DataLoading.read_compressed_bz2_json_file(self.path_prefix / 'data/test_data/test_sample_files.json.bz2')
        self.assertEqual(type(data), list)

    def test_read_compressed_bz2_json_file_when_file_isnt_bz2(self):
        try:
            DataLoading.read_compressed_bz2_json_file(self.path_prefix / 'data/test_data/test_sample_files.json')
            self.assertFalse(False)
        except ValueError:
            self.assertTrue(True)

    def test_read_compressed_bz2_json_file_when_not_json_bz2_file(self):
        try:
            DataLoading.read_compressed_bz2_json_file(self.path_prefix / 'data/test_data/test_sample_files.json.bz2')
            self.assertFalse(False)
        except ValueError:
            self.assertTrue(True)

    def test_get_twitter_data_as_bags(self):
        data = DataLoading.get_twitter_data_as_bags('../../data/test_sample_files.json.bz2')
        self.assertEqual(type(data), Bag)

    def test_get_twitter_data_from_file_list(self):
        data = DataLoading.get_twitter_data_from_file_list(['../../data/test_sample_files.json.bz2',
                                                            '../../data/test_sample_files_2.json.bz2'])
        self.assertEqual(type(data), Bag)

    def test_remove_deleted_tweets(self):
        """
        Note: Function assumes that there is a removed tweet in the first 20 tweets.
        """
        files_list = list(CommonTestSetup.get_sample_files_list())
        bags = DataLoading.get_twitter_data_as_bags(files_list, remove_deleted_tweets=False)
        removed_tweets = DataLoading.remove_deleted_tweets(bags)
        bags = bags.take(20)
        computed = removed_tweets.take(20)
        self.assertNotEqual(bags, computed)


if __name__ == "__main__":
    unittest.main()
