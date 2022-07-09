import re
# import sys
import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter
import logging


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


def download(directory, url):
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
    # except requests.exceptions.MissingSchema:
    #     logging.error('The URL scheme (e.g. http or https) is missing.')
    #     sys.exit()
    # except requests.exceptions.ConnectionError:
    #     logging.error('A Connection error occurred.')
    #     sys.exit()
    # except requests.exceptions.InvalidURL:
    #     logging.error('The URL provided was somehow invalid.')
    #     sys.exit()
    parsed_html = BeautifulSoup(html_text, 'html.parser')

    # Create a folder here
    os.mkdir(content_folder)
    # except FileNotFoundError:
    #     logging.error(f'Directory "{directory}" does not exist!')
    #     sys.exit()
    # except PermissionError:
    #     logging.error(f'Permission denied: {directory}')
    #     sys.exit()
    logging.info('Content folder created.')

    # Search for all tags and process
    for resource in parsed_html.find_all(True):

        if is_local_resource(resource, url):
            logging.info('Found local resource.')

            # Download resource file to RAM
            file_binary = requests.get(urljoin(url, get_url(resource))).content

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
            with open(os.path.join(content_folder, file_name), 'xb') \
                    as image_file:
                image_file.write(file_binary)
            logging.info('Local resource loaded.')

    # Create HTML file
    with open(html_file, mode='w') as h:
        h.write(parsed_html.prettify(formatter=UnsortedAttributes()))
    logging.info('HTML file created.')

    # Delete folder if empty
    if len(os.listdir(content_folder)) == 0:
        os.rmdir(content_folder)
        logging.info('Content folder is empty. Deleting.')

    return os.path.join(directory, html_file_name)
