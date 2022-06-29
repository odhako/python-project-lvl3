from cli_test_helpers import shell


def test_help():
    result = shell('page-loader -h')
    assert result.exit_code == 0
