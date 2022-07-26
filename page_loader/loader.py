import re
import requests
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
from progress.bar import IncrementalBar


TAG_LINK = {'img': 'src', 'link': 'href', 'script': 'src'}


def name_for(path_type, url):
    types = {'content_folder': '_files', 'html_file': '.html'}
    name = re.sub(r'\W', '-',
                  re.sub(r'(^https?://)|(/$)|\.html|\.htm', '',
                         url)) + types[path_type]
    return name


def resource_file_name(base_url, local_resource_url):
    file_name, extension = os.path.splitext(local_resource_url)
    if not extension:
        extension = '.html'
    file_name = re.sub(r'[^A-Za-z\d_\-]',
                       '-',
                       re.sub(r'^https?://',
                              '',
                              urljoin(base_url, file_name)
                              )
                       ) + extension
    return file_name


def is_local(tag, url):
    link = tag[TAG_LINK[tag.name]]

    if urlparse(link).hostname == urlparse(url).hostname:
        return True
    else:
        if link.startswith('http'):
            return False
        else:
            return True


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


def parse(html_text, url):
    logging.debug('Parsing html.')

    parsed_html = BeautifulSoup(html_text, 'html.parser')
    local_resources = []

    for resource in parsed_html.find_all(TAG_LINK.keys()):
        if is_local(resource, url):
            # Resource file local path
            local_file_path = os.path.join(
                name_for('content_folder', url),
                resource_file_name(url, resource[TAG_LINK[resource.name]])
            )

            # Add url to list for downloading
            local_resources.append({
                'file_path': local_file_path,
                'link': urljoin(url, resource[TAG_LINK[resource.name]])
            })

            # Change link to resource in parsed html
            resource[TAG_LINK[resource.name]] = local_file_path

    logging.debug(f'Found {len(local_resources)} local resources.')

    # New pretty HTML text
    output_html_text = parsed_html.prettify()

    return output_html_text, local_resources


def download_resources(resources, directory):
    # Create progress bar
    bar = IncrementalBar('Downloading:',
                         suffix='%(percent)d%% - %(eta)d seconds remaining',
                         max=len(resources))

    with bar:
        for resource in resources:
            logging.debug('Downloading local resource.')

            # Download resource file to RAM
            file_binary = requests.get(resource['link']).content

            # Create resource file
            with open(
                    os.path.join(
                        directory,
                        resource['file_path']),
                    'xb') as f:
                f.write(file_binary)
            logging.debug('Local resource loaded.')

            bar.next()


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
                directory, name_for('content_folder', url)))
        except FileNotFoundError:
            raise FileNotFoundError(f'Directory "{directory}" does not exist!')
        except PermissionError:
            raise PermissionError(f'Permission denied: {directory}')
        logging.debug('Content folder created.')

    download_resources(local_resources, directory)
    create_html_file(os.path.join(directory, name_for('html_file', url)),
                     output_html_text)

    return os.path.join(directory, name_for('html_file', url))
