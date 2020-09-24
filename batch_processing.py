"""
author: v2thegreat (v2thegreat@gmail.com)

Package to process tweets from the data_loading_tbd in batches to reduce the workload on the scheduler based on time series

TODO:
    - This package is written with the hopes to better understand what problems processing such a dataset would be
    encountered, and it is hence written with the understanding that this and other scripts will be refactored
    - Add tests
"""

from typing import Callable, Any, Dict, Iterable
from tqdm import tqdm


class Batches:

    @staticmethod
    def process_in_batches(file_paths: Iterable[str], read_func: Callable[[str], Any],
                           func_to_apply: Callable[[Any], Any],
                           verbose: bool = True) -> Dict[str, Any]:
        """
        Function to process data in batches to circumvent Dask Scheduler's limitations (max of 100k tasks for example)
        :param file_paths: path of files that need to be individually processed
        :param read_func: function to read the file. This must return an object (for example: Dask Bag, Dask Array, str)
        :param func_to_apply: function to apply on the object that's returned on the read_func
        :param verbose: show progress bar?
        :return: a dictionary that has the schema: `{file_name: func_to_apply's return value}`
        """
        file_iterator = tqdm(file_paths) if verbose else file_paths
        data_results = {}

        for file in file_iterator:
            data = read_func(file)
            data_results[file] = func_to_apply(data)

        return data_results

    @staticmethod
    def process_in_batches_generator(file_iterator: Iterable[str], read_func: Callable[[str], Any],
                                     func_to_apply: Callable[[Any], Any]) -> Iterable[Any]:
        """
        Function to process data in batches to circumvent Dask Scheduler's limitations for 100k tasks
        :param file_iterator: iterator that contains a file names
        :param read_func: function to read the file. This must return an object (for example: Dask Bag, Dask Array, str)
        :param func_to_apply: function to apply on the object that's returned on the read_func
        :return: a dictionary that has the schema: `{file_name: func_to_apply's return value}`
        """

        for file in file_iterator:
            data = read_func(file)
            yield func_to_apply(data)


if __name__ == "__main__":
    pass
