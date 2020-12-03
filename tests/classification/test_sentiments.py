import unittest

from morpheus.classification.sentiments import Sentiments
import math


class SentimentsTestCase(unittest.TestCase):
    def test_multiple_sentiment_analysis_empty(self):
        expected_output = {
            'nltk': math.nan,
            'textblob': math.nan
        }

        self.assertEqual(expected_output, Sentiments.multiple_sentiment_analysis(''))

    def test_multiple_sentiments_positive(self):
        expected_greater_than = 0
        expected_less_than = 1

        results = Sentiments.multiple_sentiment_analysis('I love this!')

        for method in results:
            self.assertTrue(expected_greater_than <= results[method] <= expected_less_than)

    def test_multiple_sentiments_negative(self):
        expected_greater_than = -1
        expected_less_than = 0

        results = Sentiments.multiple_sentiment_analysis('I hate this!')

        for method in results:
            self.assertTrue(expected_greater_than <= results[method] <= expected_less_than)

    def test_singleton(self):
        try:
            senti_1 = Sentiments()
            senti_2 = Sentiments()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
