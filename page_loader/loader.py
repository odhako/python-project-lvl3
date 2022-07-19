import re
import requests
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from progress.bar import IncrementalBar


TAG_LINK = {'img': 'src', 'link': 'href', 'script': 'src'}


def is_local(tag, url):
    link = tag[TAG_LINK[tag.name]]

    if urlparse(link).hostname == urlparse(url).hostname:
        return True
    else:
        if link.startswith('http'):
            return False
        else:
            return True


def get_url(resource):
    return resource[TAG_LINK[resource.name]]


def get_page(url):
    # Get web page
    try:
        get = requests.get(url)
    except requests.exceptions.MissingSchema:
        raise requests.exceptions.MissingSchema(
            'The URL scheme (e.g. http or https) is missing.'
        )
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError(
            'A Connection error occurred.'
        )
    except requests.exceptions.InvalidURL:
        raise requests.exceptions.InvalidURL(
            'The URL provided was somehow invalid.'
        )
    if get.status_code != 200:
        raise requests.exceptions.HTTPError(
            f'HTTP status code {get.status_code}'
        )
    return get.text


def parse_resources(bs4_soup):
    logging.debug('Parsing resources.')
    return bs4_soup(['img', 'link', 'script'])


def download_resource(resource, content_folder, url, file_name):
    # Download resource file to RAM
    file_binary = requests.get(
        urljoin(url, get_url(resource))).content

    # Create resource file
    with open(os.path.join(content_folder, file_name), 'xb') as f:
        f.write(file_binary)
    logging.debug('Local resource loaded.')


def download(url, directory):
    # Names
    directory = os.path.abspath(directory)
    html_file_name = re.sub(r'\W', '-',
                            re.sub(r'(^https?://)|(/$)|\.html|\.htm', '', url)
                            ) + '.html'
    content_folder_name = html_file_name[:-5] + '_files'
    html_file = os.path.join(directory, html_file_name)
    content_folder = os.path.join(directory, content_folder_name)

    html_text = get_page(url)
    parsed_html = BeautifulSoup(html_text, 'html.parser')

    # Create a folder here
    try:
        os.mkdir(content_folder)
    except FileNotFoundError:
        raise FileNotFoundError(f'Directory "{directory}" does not exist!')
    except PermissionError:
        raise PermissionError(f'Permission denied: {directory}')
    logging.debug('Content folder created.')

    # Search for local resources
    local_resources = [
        x for x in parse_resources(parsed_html) if is_local(x, url)
    ]

    # Create progress bar
    bar = IncrementalBar('Downloading:',
                         suffix='%(percent)d%% - %(eta)d seconds remaining',
                         max=len(local_resources))

    # Download local resources
    with bar:
        for resource in local_resources:
            logging.debug('Downloading local resource.')

            # Resource file name
            file_name, file_extension = os.path.splitext(get_url(resource))
            if not file_extension:
                file_extension = '.html'
            file_name = re.sub(r'[^A-Za-z\d_\-]',
                               '-',
                               re.sub(r'^https?://',
                                      '',
                                      urljoin(url, file_name)
                                      )
                               ) + file_extension

            # Download resource file
            download_resource(resource, content_folder, url, file_name)

            # Edit link to resource file
            resource[TAG_LINK[resource.name]] = os.path.join(
                content_folder_name, file_name)

            bar.next()

    # Create HTML file
    with open(html_file, mode='w') as h:
        h.write(parsed_html.prettify())
    logging.debug('HTML file created.')

    # Delete folder if empty
    if len(os.listdir(content_folder)) == 0:
        os.rmdir(content_folder)
        logging.debug('Content folder is empty. Deleting.')

    return os.path.join(directory, html_file_name)
