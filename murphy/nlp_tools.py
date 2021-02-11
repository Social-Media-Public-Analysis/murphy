from dask.dataframe import DataFrame as dask_dataframe
import pandas as pd
import en_core_web_sm
import nltk

from typing import Union

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    import nltk

from nltk.corpus import stopwords


class NLPTools:
    def __init__(self,
                 tokenize: bool = True,
                 filter_stopwords: bool = True,
                 lemmatize: bool = True,
                 language: str = 'english'):

        self.tokenize_flag = tokenize
        self.filter_stopwords_flag = filter_stopwords
        self.lemmatize_flag = lemmatize

        self.language = language
        self.stopwords = stopwords.words(self.language)

    nlp = en_core_web_sm.load()

    def _tokenize(self, string: str) -> str:
        tokens = nltk.word_tokenize(text=string, language=self.language)
        tokens_lst = list(filter(lambda word: word.isalnum(), tokens))
        return ' '.join(tokens_lst)

    def _remove_stopwords(self, string: str):
        filtered = filter(lambda word: word not in self.stopwords, string.split(' '))
        return ' '.join(filtered)

    @staticmethod
    def _lemmatize(string):
        doc = NLPTools.nlp(string)
        lemmatized = [token.lemma_ for token in doc]

        return ' '.join(lemmatized)

    def tokenize_tweets(self, tweet_dataframe: Union[dask_dataframe, pd.DataFrame]) -> Union[
        dask_dataframe, pd.DataFrame]:
        tweet_dataframe['text'] = tweet_dataframe['text'].apply(
            lambda text: self._tokenize(text),
            meta=str
        )
        return tweet_dataframe

    def filter_stopwords(self, tweet_dataframe: dask_dataframe) -> Union[dask_dataframe, pd.DataFrame]:
        tweet_dataframe['text'] = tweet_dataframe.apply(
            lambda x: self._remove_stopwords(x['text']),
            axis=1, meta=str
        )
        return tweet_dataframe

    def lemmatize_tweets(self, tweet_dataframe: dask_dataframe) -> Union[dask_dataframe, pd.DataFrame]:
        tweet_dataframe['text'] = tweet_dataframe.apply(
            lambda x: self._lemmatize(x['text']),
            axis=1, meta=str
        )
        return tweet_dataframe

    def run_tools(self, tweet_dataframe: dask_dataframe) -> Union[dask_dataframe, pd.DataFrame]:
        if self.tokenize_flag:
            tweet_dataframe = self.tokenize_tweets(tweet_dataframe)

        if self.filter_stopwords_flag:
            tweet_dataframe['text'] = tweet_dataframe.apply(
                lambda x: self._remove_stopwords(x['text']),
                axis=1, meta=str
            )
            # tweet_dataframe = self.filter_stopwords(tweet_dataframe)

        if self.lemmatize_flag:
            tweet_dataframe['text'] = tweet_dataframe.apply(
                lambda x: self._lemmatize(x['text']),
                axis=1,
                meta=str
            )

        return tweet_dataframe
