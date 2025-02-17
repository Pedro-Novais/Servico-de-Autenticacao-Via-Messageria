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

class FormatCredentialInvalid(Exception):
    def __init__(self):
        msg = "Senha não possui requerimentos obrigatórios"
        super().__init__(msg)
        self.msg = msg
        self.code = 400