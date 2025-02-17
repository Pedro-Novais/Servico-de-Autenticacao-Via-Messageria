import re

from app.repository._Conn import Conn

from ._CustomExceptions import (
    ParameterNotSend,
    EmailInvalid,
    FormatCredentialInvalid
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

            self.new_user(
                name=name,
                email=email,
                password=password
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