import math
from typing import Dict

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

"""
Author: v2thegreat
Source: https://medium.com/@b.terryjack/nlp-pre-trained-sentiment-analysis-1eb52a9d742c
Libraries Used:
 - NLTK
 - TextBlob
 - Flair (Depreciated due to dependency issues)
"""


class Sentiments:
    __instance__ = None

    def __init__(self):
        if Sentiments.__instance__ is None:
            Sentiments.__instance__ = self

            nltk.download('vader_lexicon', quiet=True)
            self.NLTK_SENTIMENT_INTENSITY_ANALYZER = SentimentIntensityAnalyzer()

            # Depreciated due to dependency issues
            # self.flair_sentiment = flair.models.TextClassifier.load('en-sentiment')

        else:
            raise RuntimeError(f"Singleton {self.__class__.__name__} class is created more than once!")

    @staticmethod
    def _get_instance():
        """
        Returns a singleton instance of this Sentiments class
        """
        if not Sentiments.__instance__:
            Sentiments()
        return Sentiments.__instance__

    @staticmethod
    def sentiment_analysis_nltk(text: str) -> float:
        """
        Run sentiment analysis using the library NLTK. Runs default sentiment on vader lexicon
        Works based on bag of words and positive and negative word lookups
        :param text: text to be analyzed
        :return: sentiment compound for given text
        """
        if not text:
            return math.nan

        return Sentiments._get_instance().NLTK_SENTIMENT_INTENSITY_ANALYZER.polarity_scores(text=text)['compound']

    @staticmethod
    def sentiment_analysis_textblob(text: str) -> float:
        """
        Run sentiment analysis using the library textblob. Returns default sentiment
        Works similar to NLTK's sentiment analysis, but includes subjectivity analysis
        :param text: text to be analyzed
        :return: sentiment for given text
        """
        if not text:
            return math.nan

        return TextBlob(text=text).sentiment.polarity

    _sentiment_function_mapping = {
        'nltk': sentiment_analysis_nltk.__func__,
        'textblob': sentiment_analysis_textblob.__func__
    }

    @classmethod
    def multiple_sentiment_analysis(cls, text: str) -> Dict[str, float]:
        """
        Returns the sentiment using all implemented models as a dictionary
        :param text: text to run sentiment analysis on
        :return: key pair values of name of the sentiment function and their estimations
        """
        return {sentiment: sentiment_function(text) for sentiment, sentiment_function in
                cls._sentiment_function_mapping.items()}


if __name__ == "__main__":
    pass
