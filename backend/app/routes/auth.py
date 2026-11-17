from flask import Blueprint, g, jsonify, request

from ..auth import login_required
from ..services.auth_service import (
    ContaInativa, CredenciaisInvalidas, autenticar, gerar_token,
)

bp = Blueprint("auth", __name__)


@bp.post("/auth/login")
def login():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return jsonify(erro="Envie um JSON com e-mail e senha."), 400
    email, senha = dados.get("email"), dados.get("senha")
    if not isinstance(email, str) or not isinstance(senha, str) or not email.strip() or not senha:
        return jsonify(erro="Informe e-mail e senha."), 400
    try:
        usuario = autenticar(email, senha)
    except CredenciaisInvalidas:
        return jsonify(erro="E-mail ou senha inválidos."), 401
    except ContaInativa:
        return jsonify(erro="Conta desativada. Procure a equipe da Prática Jurídica."), 403
    return jsonify(access_token=gerar_token(usuario), usuario=usuario.to_dict()), 200


@bp.get("/auth/me")
@login_required
def me():
    return jsonify(usuario=g.usuario_atual.to_dict()), 200