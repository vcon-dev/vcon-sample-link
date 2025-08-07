from server.lib.vcon_redis import VconRedis
from server.lib.logging_utils import init_logger

logger = init_logger(__name__)

default_options = {
    "custom_data": {"foo": "bar"},
    "attachment_type": "sample_data",
}


def run(vcon_uuid, link_name, opts=None):
    """Sample vcon link that adds a custom attachment"""
    logger.debug("Starting %s", link_name)

    if opts is None:
        opts = default_options

    vcon_redis = VconRedis()
    vcon = vcon_redis.get_vcon(vcon_uuid)

    # Add custom data attachment
    attachment_body = opts.get("custom_data", {"foo": "bar"})

    vcon.add_attachment(
        body=attachment_body, type=opts["attachment_type"], encoding="none"
    )

    vcon_redis.store_vcon(vcon)

    return vcon_uuid
