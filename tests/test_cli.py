import pytest
from cli_test_helpers import shell
from page_loader.scripts.run_page_loader import main

# import tempfile
# import requests_mock
# import subprocess


def test_help():
    result = shell('page-loader -h')
    assert result.exit_code == 0


def test_error():
    with pytest.raises(SystemExit):
        main()


# def test_real():
#     url = 'https://ya.ru'
#     with tempfile.TemporaryDirectory() as tempdir:
#         result = shell(f'page-loader --output {tempdir} {url}')
#         assert result.stdout.endswith('ya-ru.html\n')


# def test_with_mocking():
#     url = 'http://test.com'
#     with tempfile.TemporaryDirectory() as tempdir:
#         with requests_mock.Mocker() as m:
#             m.get(url, text='HTML')
#             result = shell(f'page-loader --output {tempdir} {url}')
#             assert result.exit_code == 0


# def test_subprocess():
#     url = 'http://test.com'
#     with tempfile.TemporaryDirectory() as tempdir:
#         with requests_mock.Mocker() as m:
#             m.get(url, text='HTML')
#             result = subprocess.run(['page-loader', '--output', tempdir, url])
#             assert result == 0
