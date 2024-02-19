import inspect
import pickle
from typing import Any, Callable, Dict

import torch
from torch.utils.data import Dataset

MAX_LENGTH = 1 << 20


class LambdaDataset(torch.utils.data.Dataset):
    def __init__(self, fn: Callable, length: int = MAX_LENGTH) -> None:
        self.length = length
        self.fn = fn

        try:
            signature = inspect.signature(fn)
            parameters = signature.parameters
            self.is_index_in_params = "index" in parameters
        except ValueError:
            self.is_index_in_params = False

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> Any:
        if self.is_index_in_params:
            return self.fn(index)
        return self.fn()


class RepeatDataset(torch.utils.data.Dataset):
    def __init__(self, dataset: Dataset, length: int = MAX_LENGTH, num_item: int = 1) -> None:
        self.length = length
        self.dataset = dataset
        self.num_item = num_item
        self.cache_item = {}

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> Any:
        index = index % self.num_item
        if index not in self.cache_item:
            self.cache_item[index] = self.dataset[index]
        return self.cache_item[index]


class PklListDataset(torch.utils.data.Dataset):
    def __init__(self, pkl_fp: str, length: int = MAX_LENGTH) -> None:
        self.length = length
        if pkl_fp.endswith(".pkl"):
            with open(pkl_fp, "rb") as f:
                self.data = pickle.load(f)
        elif pkl_fp.endswith(".pt") or pkl_fp.endswith(".pth"):
            self.data = torch.load(pkl_fp)
        else:
            raise ValueError(f"Unsupported file type: {pkl_fp}")

        self.real_length = len(self.data)

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index: int) -> Any:
        return self.data[index % self.real_length]


class PklDictDataset(PklListDataset):
    def __init__(self, pkl_fp: str, length: int = MAX_LENGTH) -> None:
        super().__init__(pkl_fp, length)
        self.keys = list(self.data.keys())

        self.real_length = min([len(self.data[key]) for key in self.keys])
        # len(self.data[self.keys[0]])

    def __getitem__(self, index: int) -> Any:
        index = index % self.real_length
        return {key: self.data[key][index] for key in self.keys}


class CombinedDictDataset(torch.utils.data.Dataset):
    def __init__(self, **datasets: Dict[str, Dataset]) -> None:
        self.datasets = datasets
        self.max_length = min([len(dataset) for dataset in datasets.values()])

    def __len__(self) -> int:
        return self.max_length

    def __getitem__(self, index: int) -> Any:
        data = {}
        for key, dataset in self.datasets.items():
            data[key] = dataset[index]
        return data
