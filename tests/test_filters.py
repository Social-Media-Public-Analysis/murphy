import unittest
from murpheus.data_loader import DataLoader
from tests import CommonTestSetup
from murpheus.filters import Filter


class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()
        self.data_loader = DataLoader(
            file_find_expression=self.path_prefix / 'data/test_data/test_sample_files.json.bz2',
            remove_emoji=False,
            remove_retweets=False,
            remove_truncated_tweets=False)
        self._test_emoji_string = 'Python is fun ❤'

    def test_is_emoji(self):
        self.assertTrue(Filter._is_emoji(self._test_emoji_string))

    def test_remove_emoji(self):
        self.assertEqual('Python is fun ', Filter._remove_emojis(self._test_emoji_string))


if __name__ == "__main__":
    unittest.main()
