# standard imports
import argparse

# copyriot imports
from .copyriot import add_header_to_file

def main():
    parser = argparse.ArgumentParser(description='Add headers to files in a directory.')
    parser.add_argument('directory_path', type=str, help='The path to the directory.')
    parser.add_argument('header_texts', type=str, nargs='+', help='One or more header texts to add.')

    args = parser.parse_args()
    for header_text in args.header_texts[::-1]:
        print(f"*************** {header_text} ***************")
        add_header_to_file(args.directory_path, header_text)

if __name__ == "__main__":
    main()
