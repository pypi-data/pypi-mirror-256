import itertools
import os
from copy import deepcopy
from os.path import join
from dataclasses import dataclass
from typing import List, Union
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
import pickle

from sklearn.linear_model import LogisticRegression

import quapy as qp
from quapy.method.aggregative import PACC
from quapy.protocol import APP, UPP
from quapy.model_selection import GridSearchQ
from quapy.method.base import BaseQuantifier


def makedirs(dir):
    print('creating ', dir)
    os.makedirs(dir, exist_ok=True)


@dataclass
class MethodDescriptor:
    id: str
    name: str
    instance: BaseQuantifier
    hyperparams: dict


class Benchmark(ABC):

    ID_SEPARATOR = '__'  # used to separate components in a run-ID, cannot be used within the component IDs

    def __init__(self, home_dir):
        self.home_dir = home_dir
        makedirs(home_dir)
        makedirs(join(home_dir, 'results'))
        makedirs(join(home_dir, 'params'))
        makedirs(join(home_dir, 'tables'))
        makedirs(join(home_dir, 'plots'))

    def _run_id(self, method: MethodDescriptor, dataset: str):
        sep = Benchmark.ID_SEPARATOR
        assert sep not in method.id, \
            (f'separator {sep} cannot be used in method ID ({method.id}), '
             f'please change the method ID or redefine {Benchmark.ID_SEPARATOR=}')
        assert sep not in dataset, \
            (f'separator {sep} cannot be used in dataset name ({dataset}), '
             f'please redefine {Benchmark.ID_SEPARATOR=}')
        return sep.join([method.id, dataset])

    def _result_path(self, method: MethodDescriptor, dataset: str):
        id = self._run_id(method, dataset)
        return join(self.home_dir, 'results', id + '.pkl')

    def _params_path(self, method: MethodDescriptor, dataset: str):
        id = self._run_id(method, dataset)
        chosen = join(self.home_dir, 'params', id + 'chosen.pkl')
        scores = join(self.home_dir, 'params', id + 'scores.pkl')
        return chosen, scores

    def _exist_run(self, method: MethodDescriptor, dataset: str):
        return os.path.exists(self._result_path(method, dataset))

    def _open_method_dataset_result(self, method: MethodDescriptor, dataset: str):
        if not self._exist_run(method, dataset):
            raise ValueError(f'cannot open result for method={method.id} and {dataset=}')

    def check_dataset(self, dataset:str):
        assert dataset in self.list_datasets(), f'unknown dataset {dataset}'

    @abstractmethod
    def list_datasets(self)-> List[str]:
        ...

    @abstractmethod
    def run_method_dataset(self, method: MethodDescriptor, dataset:str, force:bool=False, random_state=0)-> pd.DataFrame:
        ...

    def gen_tables(self):
        pass

    def gen_plots(self):
        pass

    def show_report(self, method, dataset, report: pd.DataFrame):
        id = method.id
        MAE = report['mae'].mean()
        mae_std = report['mae'].std()
        MRAE = report['mrae'].mean()
        mrae_std = report['mrae'].std()
        print(f'{id}\t{dataset}:\t{MAE=:.4f}+-{mae_std:.4f}\t{MRAE=:.4f}+-{mrae_std:.4f}')

    def run(self,
            methods: Union[List[MethodDescriptor], MethodDescriptor],
            datasets:Union[List[str],str]=None,
            force=False):

        if not isinstance(methods, list):
            methods = [methods]

        if datasets is None:
            datasets = self.list_datasets()
        elif not isinstance(datasets, list):
            datasets = [datasets]

        for method, dataset in itertools.product(methods, datasets):
            self.check_dataset(dataset)
            if not force and self._exist_run(method, dataset):
                result = pd.read_pickle(self._result_path(method, dataset))
            else:
                result = self.run_method_dataset(method, dataset, force)
            self.show_report(method, dataset, result)

        self.gen_tables()
        self.gen_plots()

    # def __add__(self, other: 'Benchmark'):
    #     this = self
    #     this_datalist = self.list_datasets()
    #     other_datalist = other.list_datasets()
    #     class CombinedBenchmark(Benchmark):
    #         def list_datasets(self) -> List[str]:
    #             return this_datalist + other_datalist
    #         def run_method_dataset(self, method: MethodDescriptor, dataset:str, force:bool=False, random_state=0) -> pd.DataFrame:
    #             if dataset in this_datalist:
    #                 run_from = this
    #             else:
    #                 run_from = other
    #             return run_from.run_method_dataset(method, dataset, force, random_state)
    #     return CombinedBenchmark()


class UCIBinaryBenchmark(Benchmark):

    def list_datasets(self)->List[str]:
        ignore = ['acute.a', 'acute.b', 'balance.2']
        return [d for d in qp.datasets.UCI_BINARY_DATASETS if d not in ignore]

    def run_method_dataset(self, method: MethodDescriptor, dataset: str, force: bool = False, random_state=0)->pd.DataFrame:

        print(f'Running method={method.id} in {dataset=}')

        qp.environ['SAMPLE_SIZE'] = 100

        q = deepcopy(method.instance)
        data = qp.datasets.fetch_UCIBinaryDataset(dataset)
        optim_for = 'mae'

        with qp.util.temp_seed(random_state):
            # data split
            train, test = data.train_test
            train, val = train.split_stratified()

            # model selection
            modsel = GridSearchQ(
                model=q,
                param_grid=method.hyperparams,
                protocol=APP(val, repeats=25),
                error=optim_for,
                refit=True,
                n_jobs=-1,
                verbose=True
            ).fit(train)

            # evaluation
            report = qp.evaluation.evaluation_report(
                model=modsel.best_model_,
                protocol=APP(test, repeats=100),
                error_metrics=qp.error.QUANTIFICATION_ERROR_NAMES
            )

            # data persistence
            chosen_path, scores_path = self._params_path(method, dataset)
            pickle.dump(modsel.best_params_, open(chosen_path, 'wb'), pickle.HIGHEST_PROTOCOL)
            pickle.dump(modsel.param_scores_, open(scores_path, 'wb'), pickle.HIGHEST_PROTOCOL)

            result_path = self._result_path(method, dataset)
            report.to_pickle(result_path)

        return report


class UCIMultiBenchmark(Benchmark):

    def list_datasets(self) -> List[str]:
        return qp.datasets.UCI_MULTICLASS_DATASETS

    def run_method_dataset(self, method: MethodDescriptor, dataset:str, force:bool=False, random_state=0) -> pd.DataFrame:

        print(f'Running method={method.id} in {dataset=}')

        qp.environ['SAMPLE_SIZE'] = 500

        q = deepcopy(method.instance)
        data = qp.datasets.fetch_UCIMulticlassDataset(dataset)
        optim_for = 'mae'

        with qp.util.temp_seed(random_state):
            # data split
            train, test = data.train_test
            train, val = train.split_stratified()

            # model selection
            modsel = GridSearchQ(
                model=q,
                param_grid=method.hyperparams,
                protocol=UPP(val, repeats=250),
                error=optim_for,
                refit=True,
                n_jobs=-1,
                verbose=True
            ).fit(train)

            # evaluation
            report = qp.evaluation.evaluation_report(
                model=modsel.best_model_,
                protocol=UPP(test, repeats=1000),
                error_metrics=qp.error.QUANTIFICATION_ERROR_NAMES
            )

            # data persistence
            chosen_path, scores_path = self._params_path(method, dataset)
            pickle.dump(modsel.best_params_, open(chosen_path, 'wb'), pickle.HIGHEST_PROTOCOL)
            pickle.dump(modsel.param_scores_, open(scores_path, 'wb'), pickle.HIGHEST_PROTOCOL)

            result_path = self._result_path(method, dataset)
            report.to_pickle(result_path)

        return report


if __name__ == '__main__':

    from quapy.benchmarking.typical import *

    # bench = UCIBinaryBenchmark('../../BenchmarkTest')
    bench = UCIMultiBenchmark('../../BenchmarkUCIMulti')
    bench.run(cc)
    bench.run(acc)
    bench.run(pacc)
    bench.run(pcc)


