from flask import (
    Flask,
    Blueprint,
    Response,
    jsonify, 
    request
    )

from redis import Redis

from manager._SendMesssage import SendMessage

class Routes:
    def __init__(self, app: Flask, redis: Redis, SendMessage: SendMessage) -> None:
        try:
            self.redis = redis
            self.send = SendMessage

            app.register_blueprint(self.route_login(), url_prefix="/api/login")
            app.register_blueprint(self.route_register(), url_prefix="/api/register")
        except Exception as e:
            print("Error creating routes from aplication: {}".format(e))

    def route_login(self) -> Blueprint:
        login_route = Blueprint("login", __name__)

        @login_route.route("", methods=["POST"])
        def _() -> Response:
            try:
                data = request.get_json()

                msg_response, code_response = self.send(self.redis, "login", data).action()

                return jsonify({"msg":msg_response}), code_response
            except Exception as e:
                return jsonify({"msg": "Erro na operação", "error": str(e)})
            
        return login_route

    def route_register(self) -> Blueprint:
        register_route = Blueprint("register", __name__)

        @register_route.route("", methods=["POST"])
        def _() -> Response:
            try:
                data = request.get_json()

                msg_response, code_response = self.send(self.redis, "register", data).action()

                return jsonify({"msg":msg_response}), code_response
            except Exception as e:
                return jsonify({"msg": "Erro na operação", "error": str(e)})

        return register_route