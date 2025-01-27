


from src.handlers.files import FileHandler
import os


class UrlHandler(FileHandler):
    def __init__(self, source, verbose=False, chunksize=10_000):
        super().__init__(source, verbose, chunksize)
        self.downloaded_file = None
        self.url = source

    def __del__(self):
        if self.downloaded_file and os.path.exists(self.downloaded_file):
            os.remove(self.downloaded_file)

    def init(self):
        # Get the name of the file from url
        file_name: str = f"/tmp/{self.source.rsplit('/', 1)[-1].strip()}"
        print(f'Downloading {file_name} ...')
        # Download file from url
        os.system(f'curl {self.source.strip()} -o {file_name}')
        print('\n')
        self.downloaded_file = file_name