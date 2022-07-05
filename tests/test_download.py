import os.path
import tempfile
import requests
import requests_mock
from page_loader import download


def test_mock():
    with requests_mock.Mocker() as m:
        m.get('http://test.com', text='resp')
        assert requests.get('http://test.com').text == 'resp'


def test_download_html_only():
    with tempfile.TemporaryDirectory() as tempdir:
        with requests_mock.Mocker() as m:
            m.get('http://test.com', text='<!DOCTYPE html>\n')
            with open(download(tempdir, 'http://test.com'), 'r') as result:
                assert result.read() == '<!DOCTYPE html>\n'


def test_download_html_and_picture():
    with tempfile.TemporaryDirectory() as tempdir:
        with open('tests/fixtures/webpage.html') as webpage:
            with requests_mock.Mocker() as m:
                m.get('http://test.com', text=webpage.read())
                m.get('http://test.com/assets/nodejs.png',
                      text='picture')
                m.get('http://test.com/assets/application.css',
                      text='css_table')
                m.get('http://test.com/courses',
                      text='html_link')
                m.get('http://test.com/packs/js/runtime.js',
                      text='js_script')
                with open(download(tempdir, 'http://test.com'), 'r') as result:
                    assert os.path.exists(
                        os.path.join(
                            tempdir,
                            'test-com_files/test-com-assets-nodejs.png'
                        )
                    )
                    with open('tests/fixtures/webpage_result.html') as expected:
                        assert result.read() == expected.read()
