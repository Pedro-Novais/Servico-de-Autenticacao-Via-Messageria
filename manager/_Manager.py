import json
from redis import Redis
from threading import Thread

class Manager:
    def __init__(self, token):
        self.redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        self.token = token

    def listen_messages(self):
        while True:
                event = self.redis_client.brpop("events_queue") 
                if event:
                    try:
                        dados_event = json.loads(event[1])
                    except Exception as e:
                        pass 
                    if dados_event["type"] in  self.token: 
                        event_id = dados_event["event_id"]
                        
                        response_action =  self.token.get(dados_event["type"])(dados_event).action()

                        self.redis_client.lpush(f"response:{event_id}", json.dumps(response_action))

    def start_listening_messages(self):
        thread = Thread(target=self.listen_messages, daemon=True)
        thread.start()