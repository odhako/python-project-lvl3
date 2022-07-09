#!/usr/bin/env python
import argparse
import sys
from os import getcwd
import requests.exceptions

from page_loader.loader import download
import logging


def main():  # noqa: C901

    file_handler = logging.FileHandler('page-loader.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d GMT%z %H:%M:%S'))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.ERROR)
    stream_handler.setFormatter(logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    ))

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d GMT%z %H:%M:%S',
                        handlers=[
                            file_handler,
                            stream_handler
                        ]
                        )
    logging.info('Script started.')

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
    try:
        print(download(args.output, args.url))
    except FileNotFoundError:
        logging.error(f'Directory "{args.output}" does not exist!')
        sys.exit()
    except PermissionError:
        logging.error(f'Permission denied: {args.output}')
        sys.exit()
    except requests.exceptions.MissingSchema:
        logging.error('The URL scheme (e.g. http or https) is missing.')
        sys.exit()
    except requests.exceptions.ConnectionError:
        logging.error('A Connection error occurred.')
        sys.exit()
    except requests.exceptions.InvalidURL:
        logging.error('The URL provided was somehow invalid.')
        sys.exit()
    logging.info('Script has finished working.')


if __name__ == "__main__":
    main()

# https://page-loader.hexlet.repl.co/
