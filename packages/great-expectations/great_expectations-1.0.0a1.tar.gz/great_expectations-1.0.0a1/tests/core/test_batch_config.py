from __future__ import annotations

from typing import Optional
from unittest.mock import Mock

import pytest

from great_expectations.core.batch_config import BatchConfig
from great_expectations.datasource.fluent.batch_request import BatchRequestOptions
from great_expectations.datasource.fluent.interfaces import DataAsset


@pytest.fixture
def mock_data_asset(monkeypatch) -> DataAsset:
    monkeypatch.setattr(DataAsset, "build_batch_request", Mock())
    data_asset: DataAsset = DataAsset(name="my_data_asset", type="table")
    data_asset._save_batch_config = Mock()

    return data_asset


@pytest.mark.unit
def test_save(mock_data_asset):
    batch_config = BatchConfig(name="test_batch_config")
    batch_config.set_data_asset(mock_data_asset)

    batch_config.save()

    mock_data_asset._save_batch_config.assert_called_once_with(batch_config)


@pytest.mark.parametrize(
    "batch_request_options",
    [
        (None,),
        ({"foo": "bar"},),
    ],
)
@pytest.mark.unit
def test_build_batch_request(
    batch_request_options: Optional[BatchRequestOptions],
    mock_data_asset: DataAsset,
):
    batch_config = BatchConfig(name="test_batch_config")
    batch_config.set_data_asset(mock_data_asset)

    batch_config.build_batch_request(batch_request_options=batch_request_options)

    mock_build_batch_request = batch_config.data_asset.build_batch_request
    assert isinstance(mock_build_batch_request, Mock)
    mock_build_batch_request.assert_called_once_with(options=batch_request_options)
