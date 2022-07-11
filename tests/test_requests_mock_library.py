import pytest
import requests
from page_loader import download
import tempfile


# # Imports for disabled tests:
# from cli_test_helpers import shell


def test_url(requests_mock):
    requests_mock.get('http://test.com', text='data')
    assert 'data' == requests.get('http://test.com').text


def test_mock_2(requests_mock):
    requests_mock.get('http://test.com', status_code=404)
    assert requests.get('http://test.com').status_code == 404


def test_with_function(requests_mock):
    requests_mock.get('http://test.com', text='data\n')
    with tempfile.TemporaryDirectory() as tempdir:
        with open(download('http://test.com', tempdir)) as result:
            assert result.read() == 'data\n'


def test_http_response_code(requests_mock):
    with tempfile.TemporaryDirectory() as tempdir:
        requests_mock.get('http://test.com', status_code=404)
        with pytest.raises(Exception,
                           match='404'):
            download('http://test.com', tempdir)


# # This test not working, going to endless cycle:
# def test_with_mocking(requests_mock):
#     url = 'http://test.com'
#     with tempfile.TemporaryDirectory() as tempdir:
#         requests_mock.get(url, text='HTML')
#         result = shell(f'page-loader --output {tempdir} {url}')
#         assert result.exit_code == 0
