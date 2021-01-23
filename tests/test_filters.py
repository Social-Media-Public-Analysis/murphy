import unittest
from murphy.data_loader import DataLoader
from tests import CommonTestSetup
from murphy.filters import Filter
import pandas as pd
import dask.dataframe as dd
from itertools import product


class FilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()
        self.data_loader = DataLoader(
            file_find_expression=self.path_prefix / 'data/test_data/test_sample_files.json.bz2',
            remove_emoji=False,
            remove_retweets_symbols=False,
            remove_truncated_tweets=False)
        self._test_emoji_string = 'Python is fun ❤'
        self._test_retweet_string = 'RT @v2thegreat:Hello people!'

    def test_is_emoji(self):
        print(self._test_emoji_string)
        print(Filter._is_emoji(self._test_emoji_string))
        self.assertTrue(Filter._is_emoji(self._test_emoji_string))
        self.assertFalse(Filter._is_emoji("This string doesn't contain an emoji"))

    def test_remove_emoji(self):
        self.assertEqual('Python is fun ', Filter._remove_emojis(self._test_emoji_string))

    def test_remove_retweet(self):
        self.assertEqual('Hello people!', Filter._remove_retweet(self._test_retweet_string))

    def test_filter_emoji(self):
        input_data = [['Python is fun ❤', 'other'], ['nick', 'other'], ['juli', 'other']]
        output_data = [['Python is fun ', 'other'], ['nick', 'other'], ['juli', 'other']]
        df = pd.DataFrame(input_data, columns=['text', 'other'])
        output_df = pd.DataFrame(output_data, columns=['text', 'other'])
        temp_df = dd.from_pandas(df, npartitions=1)
        self.assertTrue(Filter.filter_emoji(temp_df).compute().equals(output_df))

    def test_filter_retweet_text(self):
        input_data = [[self._test_retweet_string, 'other'], ['nick', 'other'], ['juli', 'other']]
        output_data = [['Hello people!', 'other'], ['nick', 'other'], ['juli', 'other']]
        df = pd.DataFrame(input_data, columns=['text', 'other'])
        output_df = pd.DataFrame(output_data, columns=['text', 'other'])
        temp_df = dd.from_pandas(df, npartitions=1)
        self.assertTrue(Filter.filter_retweet_text(temp_df).compute().equals(output_df))

    def test_remove_truncated_tweets(self):
        input_data = [['…', 'other'], ['nick', 'other'], ['juli', 'other']]
        output_data = [['nick', 'other'], ['juli', 'other']]
        df = pd.DataFrame(input_data, columns=['text', 'other'])
        output_df = pd.DataFrame(output_data, columns=['text', 'other'])
        temp_df = dd.from_pandas(df, npartitions=1)
        self.assertTrue(Filter.remove_truncated_tweets(temp_df).compute().equals(output_df))

    def test_mark_truncated_tweets(self):
        input_data = [['…', 'other'], ['nick', 'other'], ['juli', 'other']]
        df = pd.DataFrame(input_data, columns=['text', 'other'])
        df = dd.from_pandas(df, npartitions=1)
        df = Filter.mark_truncated_tweets(df)
        self.assertIn('is_truncated_tweet', df.columns)

    def test_run_filters(self):
        # runs the respective tests for when each of the flags are running
        bool_flag = [True, False]
        for emoji_flag, retweets_flag, truncated_flag in product(bool_flag, bool_flag, bool_flag):
            filter_obj = Filter(remove_emoji=emoji_flag,
                                remove_retweets=retweets_flag,
                                remove_truncated_tweets=truncated_flag)
            if emoji_flag:
                input_data = [['Python is fun ❤', 'other'], ['nick', 'other'], ['juli', 'other']]
                output_data = [['Python is fun ', 'other'], ['nick', 'other'], ['juli', 'other']]
                df = pd.DataFrame(input_data, columns=['text', 'other'])
                output_df = pd.DataFrame(output_data, columns=['text', 'other'])
                temp_df = dd.from_pandas(df, npartitions=1)
                self.assertTrue(filter_obj.run_filters(temp_df).compute().equals(output_df))

            if retweets_flag:
                input_data = [[self._test_retweet_string, 'other'], ['nick', 'other'], ['juli', 'other']]
                output_data = [['Hello people!', 'other'], ['nick', 'other'], ['juli', 'other']]
                df = pd.DataFrame(input_data, columns=['text', 'other'])
                output_df = pd.DataFrame(output_data, columns=['text', 'other'])
                temp_df = dd.from_pandas(df, npartitions=1)
                self.assertTrue(filter_obj.run_filters(temp_df).compute().equals(output_df))

            if truncated_flag:
                input_data = [['…', 'other'], ['nick', 'other'], ['juli', 'other']]
                output_data = [['nick', 'other'], ['juli', 'other']]
                df = pd.DataFrame(input_data, columns=['text', 'other'])
                output_df = pd.DataFrame(output_data, columns=['text', 'other'])
                temp_df = dd.from_pandas(df, npartitions=1)
                self.assertTrue(Filter.remove_truncated_tweets(temp_df).compute().equals(output_df))


if __name__ == "__main__":
    unittest.main()
