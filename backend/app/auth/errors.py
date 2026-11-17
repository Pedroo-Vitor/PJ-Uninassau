from flask import jsonify


def register_jwt_handlers(jwt):
    @jwt.unauthorized_loader
    def _sem_token(_m):
        return jsonify(erro="Autenticação necessária."), 401

    @jwt.invalid_token_loader
    def _invalido(_m):
        return jsonify(erro="Token inválido."), 401

    @jwt.expired_token_loader
    def _expirado(_h, _p):
        return jsonify(erro="Sessão expirada. Faça login novamente."), 401