from dask.dataframe import DataFrame as dask_dataframe
import nltk
from nltk.corpus import stopwords
import spacy


class NLPTools:
    def __init__(self,
                 tokenize: bool = True,
                 filter_stopwords: bool = True,
                 lemmatize: bool = True,
                 language='english'):
        self.tokenize_flag = tokenize
        self.filter_stopwords_flag = filter_stopwords
        self.lemmatize_flag = lemmatize

        self.language = language
        self.stopwords = stopwords.words(self.language)

    nlp = spacy.load("en_core_web_sm")

    def _tokenize(self, string: str) -> str:
        tokens = nltk.word_tokenize(text=string, language=self.language)
        tokens_lst = list(filter(lambda word: word.isalnum(), tokens))
        return ' '.join(tokens_lst)

    def remove_stopwords(self, string: str):
        filtered = filter(lambda word: word not in self.stopwords, string.split(' '))
        return ' '.join(filtered)

    @staticmethod
    def lemmatize(string):
        doc = NLPTools.nlp(string)
        lemmatized = [token.lemma_ for token in doc]

        return ' '.join(lemmatized)

    def run_functionality(self, twitter_dataframe: dask_dataframe):
        if self.tokenize_flag:
            twitter_dataframe['text'] = twitter_dataframe.apply(
                lambda x: self._tokenize(x['text']),
                axis=1, meta=str
            )

        if self.filter_stopwords_flag:
            twitter_dataframe['text'] = twitter_dataframe.apply(
                lambda x: self.remove_stopwords(x['text']),
                axis=1, meta=str
            )

        if self.lemmatize_flag:
            twitter_dataframe['text'] = twitter_dataframe.apply(
                lambda x: self.lemmatize(x['text']),
                axis=1,
                meta=str
            )

        return twitter_dataframe
