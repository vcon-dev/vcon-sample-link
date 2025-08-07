"""Test the sample link"""

from unittest.mock import patch

import pytest
from vcon import Vcon

from vcon_sample_link import run


class MockVconRedis:
    """Mock VconRedis class"""

    def __init__(self):
        self.vcon = None

    def get_vcon(self, vcon_uuid):
        if self.vcon is None:
            self.vcon = Vcon(
                vcon_dict={
                    "meta": {},
                    "parties": [],
                    "attachments": [],
                    "dialog": [],
                    "analysis": [],
                },
            )
        return self.vcon

    def store_vcon(self, vcon):
        self.vcon = vcon


@pytest.fixture
def mock_vcon_redis():
    return MockVconRedis()


@patch("vcon_sample_link.link.VconRedis")
def test_sample_link(mock_vcon_redis_class, mock_vcon_redis):
    """Test the sample link"""
    mock_vcon_redis_class.return_value = mock_vcon_redis
    vcon = mock_vcon_redis.get_vcon("test-uuid")
    assert vcon.find_attachment_by_type(type="foo_data") is None
    result = run(vcon_uuid="test-uuid", link_name="foo_link", opts={
        "custom_data": {"foo": "bar"},
        "attachment_type": "foo_data",
    })
    assert result == "test-uuid"
    vcon = mock_vcon_redis.get_vcon("test-uuid")

    attachment = vcon.find_attachment_by_type(type="foo_data")
    assert attachment is not None
    assert attachment["body"] == {"foo": "bar"}
