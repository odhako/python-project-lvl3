import requests
import requests_mock


def test_mock():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        assert requests.get('http://test.com').text == 'resp'
