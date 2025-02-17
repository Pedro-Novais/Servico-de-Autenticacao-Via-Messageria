from redis import Redis
from flask import Flask

from app.repository._Conn import Conn
from app.routes._Routes import Routes 

from loginComp.main import main_login
from registerComp.main import main_register

from manager._SendMesssage import SendMessage

def main():
    try:
        app = Flask(__name__)

        conn = Conn()

        conn.create_database()
        conn.create_table()

        redis_client = Redis(host='localhost', port=6379, decode_responses=True)
        
        Routes(app=app, redis=redis_client, SendMessage=SendMessage)
        
        main_login()
        main_register()
        
        app.run()

    except Exception as e:
        print(e)

if "__main__" == __name__:
    main()