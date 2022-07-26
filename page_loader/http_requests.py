import requests


def http_request(url):
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
    return get


def get_page(url):
    # Get web page
    return http_request(url).text


def get_resource(url):
    # Get resource file binary
    return http_request(url).content
