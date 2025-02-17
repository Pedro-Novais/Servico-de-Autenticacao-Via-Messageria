from flask import Request
from redis import Redis
import uuid
import json

class SendMessage:
    TIMEOUT =   10
    def __init__(self, redis: Redis, message_type: str, data: Request):
        self.redis = redis
        self.event_id = str(uuid.uuid4())

        self.data_action = json.dumps({
            "type": message_type, 
            "data": data,
            "event_id": self.event_id
        })
    
    def action(self):

        self.redis.lpush("events_queue", self.data_action)
        
        response_message = self.redis.brpop(f"response:{self.event_id}", timeout=self.TIMEOUT)

        try:
            if response_message and response_message[1]:
                response = json.loads(response_message[1])
                return response.get("msg"), response.get("code")
            else:
                return "Erro na operação", 500
        except Exception as e:
            pass