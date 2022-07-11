import pytest
from cli_test_helpers import shell
from page_loader.scripts.run_page_loader import main


def test_help():
    result = shell('page-loader -h')
    assert result.exit_code == 0


def test_error():
    with pytest.raises(SystemExit):
        main()
