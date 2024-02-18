
class Config:

    control_channel_project_id = None
    control_channel_topic_id = None

    @classmethod
    def setup(cls, control_channel_project_id, control_channel_topic_id):
        cls.control_channel_project_id = control_channel_project_id
        cls.control_channel_topic_id = control_channel_topic_id
        
        return cls.control_channel_project_id, cls.control_channel_topic_id
    