from abc import ABC, abstractmethod
import pandas as pd
import wget
import os


class BaseIterHandler(ABC):
    def __init__(self, source: str, verbose:bool=False, chunksize:int=10_000):
        self.source = source
        self.verbose = verbose
        self.chunksize = chunksize

    @abstractmethod
    def __iter__(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def __next__(self) -> pd.DataFrame:
        pass




