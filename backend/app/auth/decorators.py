from functools import wraps

from flask import g, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from ..extensions import db
from ..models.usuario import Usuario


def get_usuario_atual():
    try:
        return db.session.get(Usuario, int(get_jwt_identity()))
    except (TypeError, ValueError):
        return None


def role_required(*perfis):
    """@role_required("professor", "gestao"). Sem argumentos: qualquer perfil logado.
    Perfil e status ativo são lidos do banco a cada requisição."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            usuario = get_usuario_atual()
            if usuario is None or not usuario.ativo:
                return jsonify(erro="Usuário não encontrado ou inativo."), 401
            if perfis and usuario.perfil not in perfis:
                return jsonify(erro="Acesso negado para o seu perfil."), 403
            g.usuario_atual = usuario
            return fn(*args, **kwargs)
        return wrapper
    return decorator


login_required = role_required()