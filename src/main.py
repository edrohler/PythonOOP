import argparse

import sys
sys.path.append('.')

from api.app import app

def main():
    parser = argparse.ArgumentParser(description="Start the Flask app")
    parser.add_argument("--serve", action="store_true", help="Start the Flask API App")

    args = parser.parse_args()

    if args.serve:
        app.run(debug=True, use_reloader=False)

if __name__ == "__main__":
    main()