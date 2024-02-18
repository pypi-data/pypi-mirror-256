import json
from google.cloud import pubsub_v1
from config import Config

class PubSubAdapter():

    project_id = Config.control_channel_project_id
    topic_id = Config.control_channel_topic_id
    

    def __init__(self):
        if self.project_id and self.topic_id:
            self.publisher = pubsub_v1.PublisherClient()
        else:
            self.publisher = None    

    def get_topic_path(self, project_id: str, topic_id: str):
        return self.publisher.topic_path(project=project_id, topic=topic_id)

    def publish_to_control_channel(self, message, event_type):

        if not self.project_id or not self.topic_id:
            print(f"control message: {message}, event_type:{event_type}", flush=True)
            return

        topic_path = self.get_topic_path(project_id=self.project_id, topic_id=self.topic_id)
        _data = json.dumps(message).encode('utf-8')
        # print(f'control message: {_data}', flush=True)
        future = self.publisher.publish(topic=topic_path, data=_data,
                                        event_type=event_type)  # message attributes
        print(f"PubSub result: {future.result()}", flush=True)  # block the code until the message is sent
