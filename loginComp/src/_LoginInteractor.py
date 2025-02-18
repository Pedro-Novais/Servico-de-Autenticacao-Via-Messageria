import re

from app.repository._Conn import Conn

from ._CustomExceptions import (
    ParameterNotSend, 
    EmailInvalid,
    CredentialInvalid,
    EmailNotRegistered
    )

class Login:
    def __init__(self, data):
        self.data = data.get("data", None)
        self.conn = Conn()

    def action(self):
        try:
            email = self.data.get("email", None)
            password = self.data.get("password", None)

            self.validator(email=email, password=password)
            
            response = {
                "msg": "certo",
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
    
    def validator(self, email: str, password: str) -> None:
        if not email or not password:
            raise ParameterNotSend()
        
        if not self.validator_email(email=email):
            raise EmailInvalid()
        
        # if not self.validator_password(password=password):
        #     raise CredentialInvalid()
        
    def validator_email(self, email: str) -> bool:
        regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(regex, email) is not None
    
    def validator_email_exist(self, email: str) -> bool:
        try:
            with self.conn.get_connect() as conn:
                cursor = conn.cursor()

                sql = """
                    SELECT * FROM users WHERE email = ?
                """

                cursor.execute(sql, email)

                account = cursor.fetchone()

                if not account:
                    cursor.close()
                    return False
                
                return account
            
        except Exception:
            pass

    def validator_password(self, password: str) -> bool:
        return False