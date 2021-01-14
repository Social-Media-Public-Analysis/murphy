import unittest
from murpheus.data_loading import DataLoading
from tests import CommonTestSetup
from murpheus.filters import Filter


class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()

    def test_filter_dask_dataframe(self):
        data = DataLoading.get_twitter_data_as_bags(list(CommonTestSetup.get_sample_files_list())).to_dataframe()
        results = Filter.filter(rows=data, column_name='lang', like='en')
        self.assertTrue(results.compute().shape[0] != 0)

    def test_filter_list(self):
        data = {'fruit': ['apples', 'oranges', 'tomatoes'], 'quantity': [1, 5, 7]}
        result = Filter.filter(data, column_name='fruit', like='apples')
        self.assertTrue(result['fruit'].values[0] == 'apples')


if __name__ == "__main__":
    unittest.main()
