import logging
import os

from page_loader.http_requests import get_page
from page_loader.naming import make_name_from_url
from page_loader.parser import parse
from page_loader.resource_loader import download_resources


def create_html_file(html_file, html_text):
    with open(html_file, mode='w') as h:
        h.write(html_text)
    logging.debug('HTML file created.')


def download(url, directory):
    directory = os.path.abspath(directory)
    html_text = get_page(url)

    output_html_text, local_resources = parse(html_text, url)

    if local_resources:
        # Create a folder here
        try:
            os.mkdir(os.path.join(
                directory, make_name_from_url('content_folder', url)))
        except FileNotFoundError:
            raise FileNotFoundError(f'Directory "{directory}" does not exist!')
        except PermissionError:
            raise PermissionError(f'Permission denied: {directory}')
        logging.debug('Content folder created.')

    download_resources(local_resources, directory)

    html_file_name = os.path.join(directory,
                                  make_name_from_url('html_file', url))
    create_html_file(html_file_name, output_html_text)

    return os.path.join(directory, make_name_from_url('html_file', url))
