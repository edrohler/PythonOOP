import argparse

import sys
sys.path.append(".")

from api.app import create_app as api
from cli.app import create_app as cli

def parse_arguments():
    parser = argparse.ArgumentParser(description="Start the Flask app")
    parser.add_argument("--serve", action="store_true", help="Start the Flask API App")
    parser.add_argument("--cli", action="store_true", help="Start the CLI App")    
    parser.add_argument("--debug", action="store_true", help="Set debug mode")
    return parser.parse_args()
    

def main():

    args = parse_arguments()

    if args.serve and args.debug:
        app = api(debug=True, use_reloader=True)
        app.run()
    elif args.serve:
        app = api(debug=False, use_reloader=False)
        app.run()
        
    if args.cli and args.debug:
        cli(debug=True)
    elif args.cli:
        cli(debug=False)
        
    if not args.serve and not args.cli:
        print("Please specify either --serve or --cli.")

if __name__ == "__main__":
    main()