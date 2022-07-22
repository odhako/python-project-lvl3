#!/usr/bin/env python
import argparse
import sys
from os import getcwd
from page_loader.loader import download
import logging


def logging_init():
    file_handler = logging.FileHandler('page-loader.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(
        fmt='%(asctime)s %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d GMT%z %H:%M:%S'))

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
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


def main():  # noqa: C901

    logging_init()
    logging.debug('Script started.')

    parser = argparse.ArgumentParser(
        description="Downloads a web page."
    )
    parser.add_argument('--output', '-o',
                        help="Output directory, must be created before. "
                             "Default is working directory.",
                        default=getcwd())
    parser.add_argument('url',
                        help='Url address with scheme, like http://')
    args = parser.parse_args()

    logging.info(f'Requested URL: {args.url}')
    logging.info(f'Output path: {args.output}')

    try:
        download_dir = download(args.url, args.output)
    except Exception as e:
        logging.error(e)
        sys.exit(1)

    print(f'Page was downloaded as "{download_dir}"')

    logging.debug('Finish.')


if __name__ == "__main__":
    main()
