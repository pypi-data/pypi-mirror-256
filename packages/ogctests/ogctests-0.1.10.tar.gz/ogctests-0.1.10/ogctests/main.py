from pathlib import Path
import os
import pytest


class ClientOverridePlugin:
    def __init__(self, test_client):
        self.client = test_client

    @pytest.fixture(name="http_client", scope="session")
    def override_http_client(self):
        return self.client


def run_ogctests(scope: str, test_client=None):
    """Use this function to call pytest.main() on a subset of tests from the test suite.

    :param scope: The target tests to run (i.e. features/core/test_landingpage.py)
    :param test_client: Optional test client to override the default http client.
    """
    plugin = ClientOverridePlugin(test_client)
    if test_client:
        os.environ["CLIENT_OVERRIDDEN"] = "True"
    par_dir = Path(__file__).parent
    scope = str(par_dir / scope)
    exit_code = pytest.main([scope], plugins=[plugin])
    assert exit_code == 0
