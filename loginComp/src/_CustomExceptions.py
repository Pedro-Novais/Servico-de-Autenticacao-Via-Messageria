class ParameterNotSend(Exception):
    def __init__(self):
        msg = "Parametros obrigatórios não foram enviados"
        super().__init__(msg)
        self.msg = msg
        self.code = 404

class EmailInvalid(Exception):
    def __init__(self):
        msg = "Email inválido"
        super().__init__(msg)
        self.msg = msg
        self.code = 400

class CredentialInvalid(Exception):
    def __init__(self):
        msg = "Senha incorreta"
        super().__init__(msg)
        self.msg = msg
        self.code = 400