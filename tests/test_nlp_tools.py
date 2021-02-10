import unittest
from murphy.data_loader import DataLoader
from tests import CommonTestSetup
from murphy.nlp_tools import NLPTools
from itertools import product


class NLPTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, self.path_prefix = CommonTestSetup.set_data_dir_path()
        self.data_loader = DataLoader(
            file_find_expression = self.path_prefix / 'data/test_data/test_sample_files.json.bz2'
        )

        self._test_string = "From: (where's my thing) Subject: WHAT car is this!? Nntp-Posting-Host: rac3.wam.umd.edu " \
                            "Organization: University of Maryland, College Park Lines: 15 I was wondering if anyone " \
                            "out there could enlighten me on this car I saw the other day. It was a 2-door sports " \
                            "car, looked to be from the late 60s/ early 70s. It was called a Bricklin. The doors were " \
                            "really small. In addition, the front bumper was separate from the rest of the body. This " \
                            "is all I know. If anyone can tellme a model name, engine specs, years of production, " \
                            "where this car is made, history, or whatever info you have on this funky looking car, " \
                            "please e-mail. Thanks, - IL ---- brought to you by your neighborhood Lerxst ---- "

        self._tokenized_test_string = "From where my thing Subject WHAT car is this Organization University of " \
                                      "Maryland College Park Lines 15 I was wondering if anyone out there could " \
                                      "enlighten me on this car I saw the other day It was a sports car looked to be " \
                                      "from the late early 70s It was called a Bricklin The doors were really small " \
                                      "In addition the front bumper was separate from the rest of the body This is " \
                                      "all I know If anyone can tellme a model name engine specs years of production " \
                                      "where this car is made history or whatever info you have on this funky looking " \
                                      "car please Thanks IL brought to you by your neighborhood Lerxst"

        self._no_stop_word_test_string = "From: (where's thing) Subject: WHAT car this!? Nntp-Posting-Host: " \
                                         "rac3.wam.umd.edu Organization: University Maryland, College Park Lines: 15 " \
                                         "I wondering anyone could enlighten car I saw day. It 2-door sports car, " \
                                         "looked late 60s/ early 70s. It called Bricklin. The doors really small. In " \
                                         "addition, front bumper separate rest body. This I know. If anyone tellme " \
                                         "model name, engine specs, years production, car made, history, " \
                                         "whatever info funky looking car, please e-mail. Thanks, - IL ---- brought " \
                                         "neighborhood Lerxst ---- "

        self._lemmatized_string = "from : ( where be my thing ) subject : what car be this ! ? Nntp - posting - Host : " \
                                  "rac3.wam.umd.edu Organization : University of Maryland , College Park line : 15 I " \
                                  "be wonder if anyone out there could enlighten I on this car I see the other day . " \
                                  "it be a 2 - door sport car , look to be from the late 60s/ early 70 . it be call a " \
                                  "Bricklin . the door be really small . in addition , the front bumper be separate " \
                                  "from the rest of the body . this be all I know . if anyone can tellme a model name " \
                                  ", engine spec , year of production , where this car be make , history , or whatever " \
                                  "info you have on this funky look car , please e - mail . thank , - IL ---- bring to " \
                                  "you by your neighborhood Lerxst ----"

        self.nlp_tool = NLPTools()

    def test_tokenize_func(self):
        self.assertEqual(
            self.nlp_tool._tokenize(self._test_string),
            self._tokenized_test_string
        )

    def test_remove_stopwords_func(self):
        self.assertEqual(
            self.nlp_tool._remove_stopwords(self._test_string),
            self._no_stop_word_test_string
        )

    def test_lemmatize_func(self):
        self.assertEqual(
            self.nlp_tool._lemmatize(self._test_string),
            self._lemmatized_string
        )

    def test_run_nlp_tools(self):
        bool_flag = [True, False]
        for tokenize_flag, filter_stopwords_flag, lemmatize_flag in product(bool_flag, bool_flag, bool_flag):
           nlp_tool_obj = NLPTools(
               tokenize = tokenize_flag,
               filter_stopwords = filter_stopwords_flag,
               lemmatize = lemmatize_flag
           )

           if tokenize_flag:
                pass