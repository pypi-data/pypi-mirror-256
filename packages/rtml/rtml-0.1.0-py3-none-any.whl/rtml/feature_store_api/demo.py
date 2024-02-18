import os
from datetime import datetime

from rtml.feature_store_api.api import FeatureStore
from rtml.feature_store_api.types import FeatureGroupConfig


feature_store = FeatureStore(
    api_key=os.environ["HOPSWORKS_API_KEY"],
    project_name=os.environ["HOPSWORKS_PROJECT_NAME"],
)

fg_config = FeatureGroupConfig(
    name='ohlc_feature_group',
    version=3,
    description='OHLC data for crypto products',
    primary_key=['timestamp', 'product_id'],
    event_time='timestamp',
    online_enabled=True,
)
feature_group = feature_store.get_or_create_feature_group(fg_config)

count = 0
MAX_BATCH_SIZE = 2

import threading
count_lock = threading.Lock()

def run():
    global count
    while True:
        data = {
            'timestamp': int(datetime.utcnow().timestamp()),
            'product_id': 'a',
            'open': 1.0,
            'high': 1.0,
            'low': 1.0,
            'close': 1.0,
        }
        print('Writing message to online feature group')
        feature_group.write(data)

        with count_lock:
            count += 1

def materialize():
    global count
    while True:
        if count >= MAX_BATCH_SIZE:
            # start materialization job
            print('Start materialization of {} messages')
            feature_store.materialize(feature_group)
            with count_lock:
                count = 0

if __name__ == '__main__':

    # if os.getenv('MATERIALIZE_FEATURE_GROUP') is not None:
    import threading
    materialize_thread = threading.Thread(target=materialize)
    materialize_thread.start()

    run()