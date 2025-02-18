import re

from redis import Redis

from app.repository._Conn import Conn
from manager._SendMesssage import SendMessage

from psycopg2.errors import UniqueViolation

from ._CustomExceptions import (
    ParameterNotSend,
    EmailInvalid,
    FormatCredentialInvalid,
    EmailAlreadyRegistered
    )

class Register:
    def __init__(self, data):
        self.data = data.get("data", None)
        self.conn = Conn()
    
    def action(self):
        try:
            name = self.data.get("name", None)
            email = self.data.get("email", None)
            password = self.data.get("password", None)

            self.validator(
                name=name,
                email=email,
                password=password
            )

            encode_password = self.encode_password(password=password)

            self.new_user(
                name=name,
                email=email,
                password=encode_password
            )

            response = {
                "msg": "Usuário criado com sucesso",
                "code": 200
            }

            return response
        
        except Exception as e:
            msg = "Operação inválida"
            code = 500

            try:
                if e.msg:
                    msg = e.msg
                if e.code:
                    code = e.code
            except Exception as e:
                pass

            response = {
                "msg": msg,
                "code": code
            }

            return response

    def new_user(self, name: str, email: str, password: str) -> None:
        try:
            with self.conn.get_connect() as conn:
                cursor = conn.cursor()

                sql = """
                    INSERT INTO users (name, email, password)
                    VALUES (%s, %s, %s)
                """

                user_data = (name, email, password)
                cursor.execute(sql, user_data)

                conn.commit()
                cursor.close()
        except UniqueViolation:
            raise EmailAlreadyRegistered()
        except Exception:
            raise
    
    def encode_password(self, password: str) -> str:
        redis_client = Redis(host='localhost', port=6379, decode_responses=True)

        data = {
            "password": password
        }

        send_message = SendMessage(
            redis=redis_client,
            message_type="encode",
            data=None,
            data_intern=data
        )

        response = send_message.action_intern()

        if not response:
            raise

        return response

    def validator(
            self,
            name: str,
            email: str,
            password: str
            ):
        if not name or not email or not password:
            raise ParameterNotSend()
        
        if not self.validator_email(email=email):
            raise EmailInvalid()
        
        if not self.validator_password(password=password):
            raise FormatCredentialInvalid()
        
    def validator_email(self, email: str) -> bool:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None

    def validator_password(self, password: str) -> bool:
        if len(password) < 7:
            return False
        
        regex = r"^(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).*$"
        return re.match(regex, password) is not None