from murpheus.batch_processing import Batches
from murpheus.data_loader import DataLoader


def counter(tweets):
    return len(tweets)


def example_process_in_batches():
    """
    Example function to show how process_in_batches works
    :return: returns the count of tweets
    """
    files_lst = DataLoader._get_files_list('../../../data/*.json.bz2')
    results = Batches.process_in_batches(files_lst, read_func=DataLoader._read_compressed_bz2_json_file,
                                         func_to_apply=counter, verbose=False)
    return results


def example_process_in_batches_generator():
    """
    Example function to show how process_in_batches_generator works
    :return: returns the count of tweets
    """

    files_lst = DataLoader._get_files_list('../../../data/*.json.bz2')
    generator = Batches.process_in_batches_generator(files_lst, read_func=DataLoader._read_compressed_bz2_json_file,
                                                     func_to_apply=counter)
    results = list(generator)
    return results


if __name__ == "__main__":
    print()
    print("Output from process_in_batches:", example_process_in_batches())
    print("Output from process_in_batches_generator:", example_process_in_batches_generator())
    print()
