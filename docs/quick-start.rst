Quick Start Guide
=================

Installation
------------

To install murphy on your machine, just install via pip:

.. code-block:: bash

    pip install smpa-murphy


For more information on installation, check out our :ref:`install guide<installation>`.


Starting up Dask (*optional*)
-----------------------------

Using Dask is optional, and while all of our code is backwards compatible with Pandas, being able to launch your own Dask Cluster or having access to the `Dask Dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_ or for `any of it's other use cases <https://stories.dask.org/en/latest/>`_

To use Dask, simply import it's Client class and initialize with your configurations

.. code-block:: python

    from dask.distributed import Client

    client = Client(<your configs here>)
    client

You can find more information on Dask Client `here <https://distributed.dask.org/en/latest/client.html>`_


Loading the Data
----------------

You can load datasets by pointing to where they've been saved from `Dozent <https://github.com/Social-Media-Public-Analysis/dozent>`_.

The syntax for doing so is as follows:

.. code-block:: python

    from murphy import data_loader # -> Importing murphy

    data = data_loader.DataLoader(file_find_expression = 'data/test_data/*.json.bz2') # -> You can point to another location here

    twitter_dataframe = data.twitter_dataframe # -> this return a dask dataframe that is lazily computed

    twitter_dataframe

This is what your output should look like (in a jupyter notebook)

You might be thinking: *So, my data is going to just be loaded from the file? That's it?*

Nope! Looking at a snippet from the :code:`data_loader.DataLoader` documentation

.. code-block:: python

    >>> help(data_loader.DataLoader)

    class DataLoader(builtins.object)
     |  DataLoader(file_find_expression: Union[str, pathlib.Path, List[pathlib.Path]], remove_emoji: bool = True, remove_retweets_symbols: bool = True, remove_truncated_tweets: bool = True, add_usernames: bool = True, tokenize: bool = True, filter_stopwords: bool = True, lemmatize: bool = True, language: str = 'english')
     |
     |  Methods defined here:
     |
     |  __init__(self, file_find_expression: Union[str, pathlib.Path, List[pathlib.Path]], remove_emoji: bool = True, remove_retweets_symbols: bool = True, remove_truncated_tweets: bool = True, add_usernames: bool = True, tokenize: bool = True, filter_stopwords: bool = True, lemmatize: bool = True, language: str = 'english')
     |      This is where you can specify how you want to configure the twitter dataset before you start processing it.
     |
     |      :param file_find_expression: unix-like path that is used for listing out all of the files that we need
     |
     |      :param remove_emoji: flag for removing emojis from all of the twitter text
     |
     |      :param remove_retweets_symbols: flag for removing retweet strings from all of the twitter text (`RT @<retweet_username>:`)
     |
     |      :param remove_truncated_tweets: flag for removing all tweets that are truncated, as not all information can be
     |                                      found in them
     |
     |      :param add_usernames: flag for adding in the user names from who tweeted as a separate column instead of parsing
     |                            it from the `user` column
     |
     |      :param tokenize: tokenize tweets to make them easier to process
     |
     |      :param filter_stopwords: remove stopwords from the tweets to make them easier to process
     |
     |      :param lemmatize: lemmatize text to make it easier to process
     |
     |      :param language: select the language that you want to work with

Here, we can see that the DataLoader class has tons of configurable parameters that we can use to make development easier, including built in tokenization, lemmatization, and more!

These are automatically run when you compute the your `twitter_dataframe`, meaning that these functions are *automatically implemented and parallelized, right out of the box!*

Now what?
---------

Now, you can explore the data to your heart's content! We suggest looking over this `Dask Tutorial <https://tutorial.dask.org/00_overview.html>`_ if you're not familiar with Dask already, as it'll make exploring the dataset easier
