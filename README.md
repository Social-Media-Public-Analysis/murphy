# Murphy	

![Build](https://github.com/Social-Media-Public-Analysis/murpheus/workflows/Build/badge.svg)	
[![codecov](https://codecov.io/gh/Social-Media-Public-Analysis/murphy/branch/master/graph/badge.svg?token=S652XM8QA6)](https://codecov.io/gh/Social-Media-Public-Analysis/murphy)
[![Maintainability](https://api.codeclimate.com/v1/badges/3207d1f12fc95ac9162e/maintainability)](https://codeclimate.com/github/Social-Media-Public-Analysis/murpheus/maintainability)	
[![GitHub last commit](https://img.shields.io/github/last-commit/Social-Media-Public-Analysis/murpheus.svg?style=flat)]()	
[![Issues](https://img.shields.io/github/issues-raw/Social-Media-Public-Analysis/murpheus.svg?maxAge=25000)](https://github.com/Twitter-Public-Analysis/Twitter-Public-Analysis/issues)	
[![PRs Welcome!](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/Social-Media-Public-Analysis/murpheus/pulls)	


Murpheus is a powerful analysis tool that is used to analyze a ton of twitter data from the internet archive, and is built to scale from laptop hardware to massive super computer  clusters.

## Motivation

The main goal of this project is to lower the bar for entry for datascientists, researchers and anyone else who wants to analyse and study Twitter datasets. 

Keeping this in mind, we want to build a powerful toolset that can scale this massively, and with everything working right out of the box with minimal support (but if you do need any help, hop on to our [issues](https://github.com/Social-Media-Public-Analysis/murphy/issues) page!). 

## Frameworks used:

The main framework that we used is [Dask](https://dask.org/), an extremely powerful library that *provides advanced parallelism for analytics, enabling performance at scale for the tools you love*<sup>[[1]](https://dask.org/)</sup>

## Installation:

Before installing, ensure that the version of python that you're using is python>=3.6. 
We intend to support all of the latest releases of as they come out!

### Installing with PIP:

Installing with pip is as easy as:

```bash
pip install smpa-murphy
```

### Install the latest version:

Installing the latest version is also quite simple. To do so, run the following commands:

```bash
git clone https://github.com/Social-Media-Public-Analysis/murphy.git # -> clone the repo
cd murphy                                                            # -> move over to the repo
python setup.py install                                              # -> install the library directly!
```

Annddd you're done!

## Usage:

The usage is fairly straightforward:

```python
from dask.distributed import Client   # -> Importing the dask client
from murphy import data_loader

client = Client()                     # -> feel free to modify this to point to your dask cluster!


data = data_loader.DataLoader(file_find_expression='../data/test_data/*.json.bz2') # -> Here, you can change the `find_file_expression` to point to any other location where you store your twitter data!


twitter_dataframe = data.twitter_dataframe # -> this return a dask dataframe that is lazily computed
```

This is what we see in when we view `twitter_dataframe` in a jupyter cell:

<div class="output_wrapper"><div class="out_prompt_overlay prompt" title="click to scroll output; double click to hide" style=""></div><div class="output" style=""><div class="output_area"><div class="run_this_cell"></div><div class="prompt output_prompt"><bdi>Out[13]:</bdi></div><div class="output_subarea output_html rendered_html output_result" dir="auto"><div><strong>Dask DataFrame Structure:</strong></div>
<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>created_at</th>
      <th>id</th>
      <th>id_str</th>
      <th>text</th>
      <th>source</th>
      <th>truncated</th>
      <th>in_reply_to_status_id</th>
      <th>in_reply_to_status_id_str</th>
      <th>in_reply_to_user_id</th>
      <th>in_reply_to_user_id_str</th>
      <th>in_reply_to_screen_name</th>
      <th>user</th>
      <th>geo</th>
      <th>coordinates</th>
      <th>place</th>
      <th>contributors</th>
      <th>is_quote_status</th>
      <th>quote_count</th>
      <th>reply_count</th>
      <th>retweet_count</th>
      <th>favorite_count</th>
      <th>entities</th>
      <th>favorited</th>
      <th>retweeted</th>
      <th>filter_level</th>
      <th>lang</th>
      <th>timestamp_ms</th>
      <th>user_names</th>
    </tr>
    <tr>
      <th>npartitions=2</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th></th>
      <td>object</td>
      <td>int64</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>bool</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>bool</td>
      <td>int64</td>
      <td>int64</td>
      <td>int64</td>
      <td>int64</td>
      <td>object</td>
      <td>bool</td>
      <td>bool</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
      <td>object</td>
    </tr>
    <tr>
      <th></th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th></th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
  </tbody>
</table>
</div>
<div>Dask Name: assign, 60 tasks</div></div></div></div><div class="btn btn-default output_collapsed" title="click to expand output" style="display: none;">. . .</div></div>

#### Having a deeper look at `data_loader.DataLoader`

This is what we get when we run `help(data_loader)`:

```
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
```

Here, we can see that the `DataLoader` class has tons of configurable parameters that we can use to make development easier, including built in tokenization, lemmatization, and more!

### Testing:

Tests can be run after installation simply by:

`pytest tests/`

## Call for Contributions

We're currently quite early in our development cycle, and are looking for people to help us out! It can be something as simple as designing out logo, adding high level documentation, creating a website, or whatever other idea that you have! Please contact us through the issues page if you have any ideas or would like to add any improvements to our projects!
