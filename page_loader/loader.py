import re
import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
import logging
from progress.bar import IncrementalBar


class UnsortedAttributes(HTMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v


def is_local_resource(tag, url):
    if tag.name in ('img', 'link', 'script'):
        if tag.has_attr('href'):
            link = tag['href']
        elif tag.has_attr('src'):
            link = tag['src']
        else:
            return False
        if link.startswith(url):
            return True
        else:
            if link.startswith('http'):
                return False
            else:
                return True
    else:
        return False


def get_url(resource):
    return resource['src'] if resource.has_attr('src') else resource['href']


def download(url, directory):
    # Names
    directory = os.path.abspath(directory)
    html_file_name = re.sub(r'\W', '-',
                            re.sub(r'(^https?://)|(/$)|\.html|\.htm', '', url)
                            ) + '.html'
    content_folder_name = html_file_name[:-5] + '_files'
    html_file = os.path.join(directory, html_file_name)
    content_folder = os.path.join(directory, content_folder_name)

    # Getting web page
    html_text = requests.get(url).text
    parsed_html = BeautifulSoup(html_text, 'html.parser')

    # Create a folder here
    os.mkdir(content_folder)
    logging.debug('Content folder created.')

    # Create progress bar
    bar = IncrementalBar('Downloading:',
                         suffix='%(percent)d%% - %(eta)d seconds remaining',
                         max=len(parsed_html.find_all(
                             lambda x: is_local_resource(x, url)
                         )))

    # Search for all tags and process
    with bar:
        for resource in parsed_html.find_all(
                lambda x: is_local_resource(x, url)):

            logging.debug('Found local resource.')

            # Download resource file to RAM
            file_binary = requests.get(
                urljoin(url, get_url(resource))).content

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

            # Edit link to resource file
            if resource.has_attr('src'):
                resource['src'] = os.path.join(content_folder_name, file_name)
            else:
                resource['href'] = os.path.join(content_folder_name, file_name)

            # Create resource file
            with open(os.path.join(content_folder, file_name), 'xb') as f:
                f.write(file_binary)
            logging.debug('Local resource loaded.')
            bar.next()

    # Create HTML file
    with open(html_file, mode='w') as h:
        h.write(parsed_html.prettify(formatter=UnsortedAttributes()))
    logging.debug('HTML file created.')

    # Delete folder if empty
    if len(os.listdir(content_folder)) == 0:
        os.rmdir(content_folder)
        logging.debug('Content folder is empty. Deleting.')

    return os.path.join(directory, html_file_name)
