import tempfile
import requests
import requests_mock
from page_loader import download


def test_mock():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        assert requests.get('http://test.com').text == 'resp'


def test_download():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as m:
            m.get('http://test.com', text='resp')
            with open(download(tempdir, 'http://test.com'), 'r') as result:
                assert result.read() == 'resp'
