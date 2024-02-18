import logging
import os
from typing import Optional

from quixstreams import Application

logger = logging.getLogger()

def get_app(
    local_broker_address: Optional[str] = None,
    consumer_group: Optional[str] = None,
) -> Application:

    if local_broker_address is not None:
        logger.info(f"Creating Quix app for local environment")
        logger.info(f'Broker address: {local_broker_address}')
        app = Application(
            broker_address=local_broker_address,
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
            consumer_extra_config={"allow.auto.create.topics": "true"},
            producer_extra_config={"allow.auto.create.topics": "true"},
        )
    
    else:
        logger.info(f"Creating Quix app for Quix Platform")
        app = Application.Quix(
            consumer_group=consumer_group,
            auto_offset_reset="earliest",
            auto_create_topics=True,  # Quix app has an option to auto create topics
        )
    
    return app