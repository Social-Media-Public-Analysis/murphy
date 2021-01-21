import unittest
from murpheus.data_loader import DataLoader
from tests import CommonTestSetup
from murpheus.filters import Filter


class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()
        self.data_loader = DataLoader(
            file_find_expression=self.path_prefix / 'data/test_data/test_sample_files.json.bz2')

    def test_filter_dask_dataframe(self):
        data = self.data_loader.twitter_dataframe
        results = Filter.filter(rows=data, column_name='lang', like='en')
        self.assertTrue(results.compute().shape[0] != 0)

    def test_filter_list(self):
        data = {'fruit': ['apples', 'oranges', 'tomatoes'], 'quantity': [1, 5, 7]}
        result = Filter.filter(data, column_name='fruit', like='apples')
        self.assertTrue(result['fruit'].values[0] == 'apples')


if __name__ == "__main__":
    unittest.main()
