import unittest
from murpheus.batch_processing import Batches
from murpheus.data_loading import DataLoading
from tests import CommonTestSetup


class BatchProcessingTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.data_path, _ = CommonTestSetup.set_data_dir_path()

    def test_process_in_batches(self):
        files_lst = DataLoading.get_files_list(self.data_path)
        results = Batches.process_in_batches(files_lst, read_func=DataLoading.read_compressed_bz2_json_file,
                                             func_to_apply=len, verbose=False)
        print(results)
        self.assertTrue(set(results.values()) == {5758, 5480})

    def test_process_in_batches_generator(self):
        files_lst = DataLoading.get_files_list(self.data_path)
        results = Batches.process_in_batches_generator(file_iterator=files_lst,
                                                       read_func=DataLoading.read_compressed_bz2_json_file,
                                                       func_to_apply=len)
        results = list(results)
        self.assertTrue(set(results), {5758, 5480})

    def test_singleton(self):
        try:
            batch_1 = Batches()
            batch_1 = Batches()
            self.assertTrue(False)
        except RuntimeError:
            self.assertTrue(True)
