#!/usr/bin/env python
import argparse
from os import getcwd
from page_loader.loader import download


def main():
    parser = argparse.ArgumentParser(
        description="Downloads a web page."
    )
    parser.add_argument('--output',
                        help="Output directory, must be created before. "
                             "Default is working directory.",
                        default=getcwd())
    parser.add_argument('url',
                        help='Url address with scheme, like http://')
    args = parser.parse_args()
    print(download(args.output, args.url))


if __name__ == "__main__":
    main()

# https://page-loader.hexlet.repl.co/
