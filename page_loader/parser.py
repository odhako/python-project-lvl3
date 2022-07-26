import logging
import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

from page_loader.naming import make_name_from_url, resource_file_name


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


def parse(html_text, url):
    logging.debug('Parsing html.')

    parsed_html = BeautifulSoup(html_text, 'html.parser')
    local_resources = []

    for resource in parsed_html.find_all(TAG_LINK.keys()):
        if is_local(resource, url):
            # Resource file local path
            local_file_path = os.path.join(
                make_name_from_url('content_folder', url),
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
