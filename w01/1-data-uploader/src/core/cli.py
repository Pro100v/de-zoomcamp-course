import argparse
from pathlib import Path

def parse_args():
    """
    Parse command-line arguments for the data uploader script.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    Arguments:
        --verbose, -v (store_true): Enable verbose mode.
        --yes, -y (store_true): Automatic yes to prompts.
        --user, -U (str, required): Username for Postgres.
        --password, -P (str, required): Password to the username for Postgres.
        --host (str, required): Hostname for Postgres.
        --port, -p (str, required): Port for Postgres connection.
        --db, -d (str, required): Database name for Postgres.
        --tb (str, required, action='append'): Destination table name for Postgres, according to the specified file or link order.
        --url, -u (str, action='append, mutually exclusive with --file): URL for downloads file.
        --file, -f (str, action='append, mutually exclusive with --url): Path to the input file.
    """
    parser = argparse.ArgumentParser(description="Data uploader script")    
    
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose mode')    
    parser.add_argument('--yes', '-y', action='store_true', help='Automatic yes to prompts')
    parser.add_argument('--user', '-U', type=str, required=True, help='Username for Postgres.')
    parser.add_argument('--password', '-P', type=str, required=True, help='Password to the username for Postgres.')
    parser.add_argument('--host', type=str, required=True, help='Hostname for Postgres.')
    parser.add_argument('--port', '-p', type=str, required=True, help='Port for Postgres connection.')
    parser.add_argument('--db', '-d', type=str, required=True, help='Databse name for Postgres')
    parser.add_argument('--tb', type=str, required=True, action='append', help='Destination table name for Postgres, according to the specified file or link order.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', '-u', type=str, action='append', help='URL for downloads file.')
    group.add_argument('--file', '-f', type=str, action='append', help='Path to the input file')
    
    return parser.parse_args()


def check_args(args: argparse.Namespace) -> bool:
    """
    Validates the command-line arguments passed to the script.

    Args:
        args (argparse.Namespace): The arguments parsed from the command line.

    Raises:
        ValueError: If any of the following conditions are met:
            - A URL does not start with 'http'.
            - A specified file does not exist.
            - The number of tables does not match the number of URLs or files.

    Returns:
        bool: True if all arguments are valid.

    Prints:
        A message indicating that the arguments are valid if the verbose flag is set.
    """
    if args.url:
        for url in args.url:
            if not url.startswith('http'):
                raise ValueError(f"Invalid URL: {url}")
            if url.split('.')[-1] not in ['csv', 'parquet']:
                raise ValueError(f"Invalid file format: {url}. Only CSV and Parquet files are supported.")
    if args.file:
        for file in args.file:
            if not Path(file).exists():
                raise ValueError(f"File not found: {file}")
            if file.split('.')[-1] not in ['csv', 'parquet']:
                raise ValueError(f"Invalid file format: {file}. Only CSV and Parquet files are supported")
    if len(args.tb) != len(args.url or args.file):
        raise ValueError("Number of tables must match number of URLs or files.")
    if args.verbose:
        print("Arguments are valid.")
    return True
    
    
def confirm_args(args: argparse.Namespace) -> bool:
    """
    Confirms the arguments provided for uploading data to the database.

    This function prints the details of the arguments, including the PostgreSQL connection link,
    URLs, files, and their corresponding tables. It then prompts the user to confirm if the 
    arguments are correct unless the `--yes` flag is provided.

    Args:
        args (argparse.Namespace): The arguments provided by the user, which should include:
        
            - user (str): The PostgreSQL username.
            - password (str): The PostgreSQL password.
            - host (str): The PostgreSQL host.
            - port (int): The PostgreSQL port.
            - db (str): The PostgreSQL database name.
            - url (list of str, optional): List of URLs to upload data from.
            - file (list of str, optional): List of file paths to upload data from.
            - tb (list of str): List of table names corresponding to the URLs or files.
            - yes (bool): Flag to automatically confirm the arguments without prompting.

    Returns:
        bool: True if the arguments are confirmed by the user or the `--yes` flag is provided, 
              False otherwise.
    """
    def print_args(args: argparse.Namespace):
        print("\nIt will be upload data to the DB:")
        postgres_link = f"postgresql://{args.user}:{args.password}@{args.host}:{args.port}/{args.db}"
        print(f"\tPostgres Link: {postgres_link}")
        print("For each URL or file, it will be uploaded to the following tables:")
        if args.url:
            for url, tb in zip(args.url, args.tb):
                print(f"\tURL: {url} -> Table: {tb}")
        if args.file:
            for file, tb in zip(args.file, args.tb):
                print(f"\tFile: {file} -> Table: {tb}")
        print()
    print_args(args)
    if not args.yes:
        confirm = input("\n\nAre these arguments correct? (y/n): ")
        result = confirm.lower() == 'y'
    else:
        result = True
    return result