Murphy Use Case
===============

1. First and foremost, Murphy is designed to be *scalable*.

2. Second, Murphy is designed with functionality in mind, and we hope it becomes the first tool people like you use to play with, understand, and visualize your data.

3. Finally, you also have access to the flexibility of `Dask DataFrames <https://docs.dask.org/en/latest/dataframe.html>`_ after we're done with it, so you can do whatever you want after using Murphy, including `switching over to Spark <https://docs.dask.org/en/latest/spark.html#reasons-to-choose-both>`_.


Work with Data from *Dozent: the best twitter scraper*
-------------------------------------------------------------
The twitter data you can get from `Dozent <https://github.com/Social-Media-Public-Analysis/dozent>`_ is extremely large, estimated to be **52.56TB per year** and while we support data from 2017 to 2020 we intend to support more data later on. In comparison, the `GDELT Project <https://www.gdeltproject.org/>`_ only works with 2.5TB of data yearly (But they do some amazing work! Seriously, check them out!)

An Exempt from Dozent's README:

.. code-block:: markdown

    Dozent

    Dozent is a powerful downloader that is used to collect large amounts of Twitter data from the
    internet archive.

    It is built on top of PySmartDL and multithreading, similar to how traditional download accelerators
    like axel, aria2c and aws s3 work, ensuring that the biggest bottlenecks are your network and your
    hardware.

    The data that is downloaded is already heavily compressed to reduce download times and save local
    storage. When uncompressed, the data can easily add up to several terabytes depending on the
    timeframe of data being collected.


Built-in tools, made to scale
----------------------------

Complex Algorithms
++++++++++++++++++

Murphy comes prepackaged with scalable and efficient implementations of various algorithms that you already use for NLP type tasks, such as tokenization, lemmatization, functionality to remove emojis, redundant and annoyingly irrelevant information and more!


Machine Learning Models
+++++++++++++++++++++++

Murphy implements simple ML models such as sentiment classification along with various different versions that might suit your best needs. While this is quite limited right now, we are actively working on deploying more ML models that can provide more insight into this dataset

.. list-table:: Machine Learning Models
    :header-rows: 1

    * - ML Model
      - Category
      - Function
      - Availability
    * - NLTK
      - Classification
      - Sentiment Prediction, built using `NLTK <https://www.nltk.org/>`_
      - |:heavy_check_mark:|
    * - TextBlob
      - Classification
      - Sentiment Prediction, built using `TextBlob <https://textblob.readthedocs.io/en/dev/>`_
      - |:heavy_check_mark:|
    * - Emoji Predictor
      - Classification
      - Predicting the best emoji for a sentence
      - |:watch:|