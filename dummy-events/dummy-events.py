import json
from random import randrange
import time
import datetime
from google.cloud.pubsublite.cloudpubsub import PublisherClient
from google.cloud.pubsublite.types import (
    CloudRegion,
    CloudZone,
    MessageMetadata,
    TopicPath,
)

# TODO(developer):
project_number = 901609931486
cloud_region = "us-central1"
# zone_id = "a"
topic_id = "testTopic"
regional = True

if regional:
    location = CloudRegion(cloud_region)
else:
    location = CloudZone(CloudRegion(cloud_region), zone_id)

topic_path = TopicPath(project_number, location, topic_id)
print(topic_path)

# PublisherClient() must be used in a `with` block or have __enter__() called before use.
with PublisherClient() as publisher_client:
    # data = "Hello world!"
    # api_future = publisher_client.publish(topic_path, data.encode("utf-8"))
    # # result() blocks. To resolve API futures asynchronously, use add_done_callback().
    # message_id = api_future.result()
    # message_metadata = MessageMetadata.decode(message_id)
    # print(message_metadata)
    # print(
      # f"Published a message to {topic_path} with partition {message_metadata.partition.value} and offset {message_metadata.cursor.offset}."
    # )

    data = json.load(open("./data_stream/events.json", 'r'))
    for row in data:
        now = datetime.datetime.now()
        row['event_date'] = now.strftime("%Y-%m-%d %H:%M:%S")
        data = json.dumps(row).encode("utf-8")
        api_future = publisher_client.publish(topic_path, data=data)
        message_id = api_future.result()
        message_metadata = MessageMetadata.decode(message_id)
        print(f"Published a {data} to {topic_path} with partition {message_metadata.partition.value} and offset {message_metadata.cursor.offset}.")
        time.sleep(randrange(1, 10))

