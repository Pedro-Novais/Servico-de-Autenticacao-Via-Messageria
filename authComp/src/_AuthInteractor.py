class Auth:
    def __init__(self, data):
        pass

    def action(self):
        try:
            response = {
                "msg": "certo auth",
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