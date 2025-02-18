from flask import Request
from redis import Redis
import uuid
import json

class SendMessage:
    TIMEOUT =   10
    TIMEOUT_INTERN =   20
    def __init__(self, redis: Redis, message_type: str, data: Request | None, data_intern: dict | None = None):
        self.redis = redis
        self.event_id = str(uuid.uuid4())

        self.data_action = json.dumps({
            "type": message_type, 
            "data": data_intern if data_intern else data,
            "event_id": self.event_id
        })
    
    def action(self) -> tuple[str, int]:

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

    def action_intern(self):
        self.redis.lpush("events_queue", self.data_action)
        
        response_message = self.redis.brpop(f"response:{self.event_id}", timeout=self.TIMEOUT_INTERN)

        try:
            if response_message and response_message[1]:
                response = json.loads(response_message[1])
                return response.get("response")
            else:
                return None
        except Exception as e:
                return None