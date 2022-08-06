import logging
from progress.bar import IncrementalBar

from page_loader.filesystem_io import create_resource_file
from page_loader.http_requests import get_resource


def download_resources(resources, directory):
    # Create progress bar
    bar = IncrementalBar('Downloading:',
                         suffix='%(percent)d%% - %(eta)d seconds remaining',
                         max=len(resources))

    with bar:
        for resource in resources:
            logging.debug('Downloading local resource.')

            # Download resource file to RAM
            file_binary = get_resource(resource['link'])

            # Create resource file
            create_resource_file(file_binary, directory, resource['file_path'])
            logging.debug('Local resource loaded.')

            bar.next()
