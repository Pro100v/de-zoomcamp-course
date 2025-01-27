import pyarrow.parquet as pq
import pandas as pd

from src.handlers.base import BaseIterHandler


class FileHandler(BaseIterHandler):
    def __init__(self, source, verbose=False, chunksize:int=10_000):
        super().__init__(source, verbose, chunksize)
        self.iterator = None
        self._df_sample = None

    def __iter__(self):
        if self.iterator is None:
            self.init()
        return self

    def __next__(self):
        if self.iterator is None:
            self.init()
        batch = next(self.iterator)
        if self.source_type == 'parquet':
            batch = batch.to_pandas()
        if not isinstance(batch, pd.DataFrame):
            raise ValueError("Invalid data type. Only Pandas DataFrames are supported.")
        return batch
    
    @property
    def source_type(self):
        return self.source.split('.')[-1]
    
    def get_sample(self) -> pd.DataFrame:
        return self._df_sample or pd.DataFrame()
    
    def init(self):
        ftype = self.source_type
        if ftype == 'csv':
            self._df_sample = pd.read_csv(self.source, nrows=5)
            self.iterator = pd.read_csv(self.source, iterator=True, chunksize=self.chunksize)
        elif ftype == 'parquet':
            file = pq.ParquetFile(self.source)
            self._df_sample = next(file.iter_batches(batch_size=5)).to_pandas()
            self.iterator = file.iter_batches(batch_size=100000)
        else:
            raise ValueError(f"Invalid file format: {self.source}. Only CSV and Parquet files are supported.")       
        
        return self