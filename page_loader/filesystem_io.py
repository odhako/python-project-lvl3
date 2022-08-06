import logging
import os

from page_loader.naming import make_name_from_url


def create_html_file(html_file, html_text):
    try:
        with open(html_file, mode='w') as h:
            h.write(html_text)
    except FileNotFoundError:
        raise FileNotFoundError(
            f'Directory "{os.path.dirname(html_file)}" does not exist!')
    except PermissionError:
        raise PermissionError(
            f'Permission denied: {os.path.dirname(html_file)}')
    logging.debug('HTML file created.')


def create_resource_folder(url, directory):
    try:
        os.mkdir(os.path.join(
            directory, make_name_from_url('content_folder', url)))
    except FileNotFoundError:
        raise FileNotFoundError(f'Directory "{directory}" does not exist!')
    except PermissionError:
        raise PermissionError(f'Permission denied: {directory}')
    logging.debug('Content folder created.')


def create_resource_file(file_binary, directory, file_path):
    with open(os.path.join(directory, file_path), 'xb') as f:
        f.write(file_binary)
