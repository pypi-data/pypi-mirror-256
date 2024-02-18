from .utils.log_config import setup_logging

from .dataset.tabledata.titanic import titanic_data
from .dataset.cv.cifar10 import cifar10_data

from .metrix.binary_classification import binary_classification, binary_classification_objective
from .metrix.multiclass_classificatio import multiclass_classification, multiclass_classification_objective

from .train.optuna import exec_optuna
from .train.load_method import load_method_from_path
import shutil

result_logger, _ = setup_logging()


class AutoResEvaluator():
    def __init__(
            self,
            dataset_name,
            model_path,
            params,
            valuation_index,
            datasave_path
            ) -> None:
        self.dataset_name = dataset_name
        self.model_path = model_path
        self.params = params
        self.valuation_index = valuation_index
        self.datasave_path = datasave_path
        self._select_dataset()
        self.model = None
        pass

    def _select_dataset(self):
        if self.dataset_name == 'titanic':
            self.datatype = 'table'
            self.train_dataloader, self.test_dataloader= titanic_data()
            self.metrix = binary_classification
            self.objective = binary_classification_objective(self.valuation_index)
        elif self.dataset_name == 'cifar10':
            self.datatype = 'image'
            self.train_dataloader, self.test_dataloader = cifar10_data(self.datasave_path)
            self.metrix = multiclass_classification
            self.objective = multiclass_classification_objective(self.valuation_index)

    def _copy_file(self):
        last_slash_index = self.model_path.rfind('/')
        directory_path = self.model_path[:last_slash_index + 1]
        copy_file_path = directory_path + 'copy_file.py'
        shutil.copyfile(self.model_path, copy_file_path)

        return copy_file_path

    def exec(self):
        result_logger.info('------AutoRes Evaluator Start------')
        result_logger.info(f'dataset name: {self.dataset_name}')
        result_logger.info(f'data type: {self.datatype}')
        result_logger.info(f'model path: {self.model_path}')
        result_logger.info(f'valuation_index: {self.valuation_index}')
        result_logger.info(f'objective: {self.objective}')
        self.copy_file_path = self._copy_file()

        exec_optuna(
            self.copy_file_path,
            self.train_dataloader,
            self.test_dataloader,
            self.metrix,
            self.params,
            self.valuation_index,
            self.objective,
            self.datatype
            )
        pass
