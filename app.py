from redis import Redis
from flask import Flask

from app.repository._Conn import Conn
from app.routes._Routes import Routes 

from manager._Manager import Manager
from manager._ManagerIntern import ManagerIntern
from tokens.Tokens import TOKENS
from tokens.TokensIntern import TOKENS_INTERN

from manager._SendMesssage import SendMessage

def main():
    try:
        app = Flask(__name__)

        conn = Conn()

        conn.create_database()
        conn.create_table()

        redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        
        Routes(app=app, redis=redis_client, SendMessage=SendMessage)
        
        manager = Manager(token=TOKENS)
        manager_intern = ManagerIntern(token=TOKENS_INTERN)
        
        manager.start_listening_messages()
        manager_intern.start_listening_messages_intern()

        app.run()

    except Exception as e:
        print(e)

if "__main__" == __name__:
    main()