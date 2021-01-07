"""
author: v2thegreat (v2thegreat@gmail.com)

Package to filter out irrelevant rows that might not be wanted for processing

TODO:
    - This package is written with the hopes to better understand what problems processing such a dataset would be
    encountered, and it is hence written with the understanding that this and other scripts will be refactored
    - Add tests
"""

from typing import Union, List, Dict, Any
import pandas as pd
from dask.dataframe import DataFrame as dask_Dataframe


class Filter:
    __instance__ = None

    def __init__(self):
        """
        Create Filter object that can filter out unneeded rows
        """
        pass

    @staticmethod
    def filter(rows: Union[List[Dict], Dict[str, List], pd.DataFrame, dask_Dataframe], column_name: str = None,
               like: Any = None) -> Union[dask_Dataframe, pd.DataFrame]:
        """
        Function to filter out rows that don't match.

        :param rows: rows that need to be filtered out
        :param column_name: name of the column to match against
        :param like: what the object is supposed to look like when converted to a string
        :return:
        """

        if type(rows) == dict or type(rows) == list:
            _data = pd.DataFrame(rows)
        else:
            _data = rows

        return _data[_data[column_name] == like]


if __name__ == "__main__":
    pass
