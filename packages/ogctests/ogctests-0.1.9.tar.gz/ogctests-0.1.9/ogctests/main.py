import os
from pathlib import Path

import pytest

root_dir = Path(__file__).parent


def run_features_core(instance_url: str, test_client):
    os.environ["INSTANCE_URL"] = instance_url
    os.environ["OGC_CALLED_FROM_PREZ"] = True
    pytest.main(args=[str(root_dir / "features/core")])
