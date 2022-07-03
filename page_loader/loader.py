import re
import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def download(directory, url):
    # Names
    directory = os.path.abspath(directory)
    file_name = re.sub(r'\W', '-',
                       re.sub(r'(^https?://)|(/$)|\.html|\.htm', '', url)
                       ) + '.html'
    content_folder_name = file_name[:-5] + '_files'
    html_file = os.path.join(directory, file_name)
    content_folder = os.path.join(directory, content_folder_name)

    # Create a folder here
    os.mkdir(content_folder)

    html_text = requests.get(url).text
    parsed_html = BeautifulSoup(html_text, 'html.parser')

    # Search for image tags and process
    for image in parsed_html.find_all('img'):

        # Only local files
        if image['src'].startswith('http'):
            pass
        else:
            # Download image to RAM
            image_binary = requests.get(urljoin(url, image['src'])).content

            # Image file name
            image_name, image_extension = os.path.splitext(image['src'])
            image_name = re.sub(r'[^A-Za-z\d_\-]',
                                '-',
                                re.sub(r'^https?://',
                                       '',
                                       urljoin(url, image_name)
                                       )
                                ) + image_extension

            # Edit link to image
            image['src'] = os.path.join(content_folder_name, image_name)

            # Create image file
            with open(os.path.join(content_folder, image_name), 'xb') \
                    as image_file:
                image_file.write(image_binary)

    # Create HTML file
    with open(html_file, mode='w') as h:
        h.write(parsed_html.prettify())
    return os.path.join(directory, file_name)
