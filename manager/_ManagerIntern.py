import json
from redis import Redis
from threading import Thread

import time

class ManagerIntern:
    def __init__(self, token):
        self.redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        self.token = token

    def listen_messages_intern(self):
        while True:
            event = self.redis_client.brpop("events_queue") 
            if event:
                try:
                    dados_event = json.loads(event[1])
                except Exception as e:
                    print("erro: {}".format(e))
                    pass

                if dados_event["type"] in  self.token: 
                    event_id = dados_event["event_id"]
                    
                    response_action =  self.token.get(dados_event["type"])(dados_event).action()

                    self.redis_client.lpush(f"response:{event_id}", json.dumps(response_action))

    def start_listening_messages_intern(self):
        thread = Thread(target=self.listen_messages_intern, daemon=True)
        thread.start()