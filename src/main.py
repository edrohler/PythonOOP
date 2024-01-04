import argparse

import sys
sys.path.append('.')

from api.app import app

def main():
    parser = argparse.ArgumentParser(description="Start the Flask app")
    parser.add_argument("--serve", action="store_true", help="Start the Flask API App")
    parser.add_argument("--debug", action="store_true", help="Set debug mode")

    args = parser.parse_args()

    if args.serve:
        app.run(debug=False, use_reloader=False)
    elif args.serve and args.debug:
        app.run(debug=True, use_reloader=True)

if __name__ == "__main__":
    main()