"""Global pytest configuration and fixtures."""

import sys
from unittest.mock import Mock

# Mock the server modules that don't exist in test environment
sys.modules['server'] = Mock()
sys.modules['server.lib'] = Mock()
sys.modules['server.lib.vcon_redis'] = Mock()
sys.modules['server.lib.logging_utils'] = Mock()
sys.modules['server.lib.metrics'] = Mock()
sys.modules['server.links'] = Mock()

# Create mock classes
mock_vcon_redis = Mock()
mock_init_logger = Mock()
mock_init_metrics = Mock()

# Configure the mocks
sys.modules['server.lib.vcon_redis'].VconRedis = mock_vcon_redis
sys.modules['server.lib.logging_utils'].init_logger = mock_init_logger
sys.modules['server.lib.metrics'].init_metrics = mock_init_metrics
