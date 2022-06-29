import re
import requests
import os


def download(directory, url):
    r = requests.get(url)
    filename = re.sub(r'\W', '-',
                      re.sub(r'(^https?://)|(/$)|html|htm', '', url)
                      ) + '.html'
    file = os.path.join(directory, filename)

    with open(file, mode='w') as html_file:
        html_file.write(r.text)
    print(os.path.join(directory, filename))
