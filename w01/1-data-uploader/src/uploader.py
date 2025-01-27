from time import time
from sqlalchemy import create_engine

from src.handlers.files import FileHandler
from src.handlers.urls import UrlHandler

import logging 


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



class Uploader(object):
    def __init__(self, user: str, password: str, host: str, port: str, db: str, tb: list[str], url: list[str]|None, file: list[str]|None, verbose: bool = False):        
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db = db
        self.tbls = tb
        self.urls = url
        self.files = file
        self.verbose = verbose
        self.handler = FileHandler if self.files else UrlHandler

        if self.verbose:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        
    def execute(self):

        sources = self.files or self.urls 
        if self.files:
            sources = self.files
        if self.urls:
            sources = self.urls
        else:
            raise ValueError('No sources provided')

        logger.debug(f'sources: {sources}')
        engine = create_engine(f'postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}')
        logger.debug(f'engine: {engine}')

        for source, table in zip(sources, self.tbls):

            itter = self.handler(source, self.verbose, chunksize=10_000).init()            
            sample = itter.get_sample()

            # Create the table
            if sample:
                sample.head(0).to_sql(name=table, con=engine, if_exists='replace')
            else:
                raise ValueError('No sample data available. Create table is broken')
            
            # Insert values
            t_start = time()
            count = 0
            for count, batch_df in enumerate(itter):

                print(f'inserting batch {count+1}...')

                b_start = time()
                batch_df.to_sql(name=table, con=engine, if_exists='append')
                b_end = time()

                print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')
                
            t_end = time()   
            print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    
            


def main():
    uploader = Uploader(
        user="postgres",
        password="postgres",
        host="localhost",
        port="5433",
        db="ny_taxi",
        tb=["test"],
        file=["/home/student/edu/zoomcamp/de-zoomcamp-course/w01/data/taxi+_zone_lookup.csv"],
        url=None,
        verbose=True
    )
    uploader.execute()

if __name__ == "__main__":
    main() 