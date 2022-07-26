import os
import re
from urllib.parse import urljoin


def make_name_from_url(path_type, url):
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
