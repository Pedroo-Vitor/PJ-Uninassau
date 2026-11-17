from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.usuario import Usuario


class CredenciaisInvalidas(Exception):
    pass


class ContaInativa(Exception):
    pass


# Evita revelar por tempo de resposta quais e-mails existem.
_HASH_FALSO = generate_password_hash("senha-descartavel")


def autenticar(email: str, senha: str) -> Usuario:
    email = (email or "").strip().lower()
    usuario = db.session.scalar(db.select(Usuario).filter_by(email=email))
    if usuario is None:
        check_password_hash(_HASH_FALSO, senha or "")
        raise CredenciaisInvalidas()
    if not usuario.check_senha(senha or ""):
        raise CredenciaisInvalidas()
    if not usuario.ativo:
        raise ContaInativa()
    return usuario


def gerar_token(usuario: Usuario) -> str:
    return create_access_token(
        identity=str(usuario.id), additional_claims={"perfil": usuario.perfil}
    )