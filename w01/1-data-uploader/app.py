import sys
import src.core.cli as cli
from src.uploader import Uploader



def main():
    args = cli.parse_args()
    
    if args.verbose:
        print(f"Input file: {args.input}")
        print(f"Output file: {args.output}")
        
    # print()
    # print(args)
    # d = dict(args.__dict__)
    # print(d)
    
    
    cli.check_args(args)
    if not cli.confirm_args(args):
        sys.exit(1)
    else:
        print("Proceeding with data upload...")

    uploader = Uploader(**args.__dict__)
    uploader.execute()
    
    
    # Your main logic here

if __name__ == "__main__":
    main()