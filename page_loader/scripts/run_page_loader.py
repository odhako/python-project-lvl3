#!/usr/bin/env python
import argparse


def main():
    parser = argparse.ArgumentParser(
        description="Downloads a web page."
    )
    parser.add_argument('--output',
                        help="Output directory, must be created before. "
                             "Default is working directory.",
                        default='default')
    parser.add_argument('url',
                        help='Url address with scheme, like http://')
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
