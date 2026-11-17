"""Seed inicial: um usuário de cada perfil, só para desenvolvimento.

Uso (com as migrações já aplicadas):
    python seed.py
"""
import os

from app import create_app
from app.extensions import db
from app.models.usuario import (
    PERFIL_ALUNO,
    PERFIL_ASSISTIDO,
    PERFIL_GESTAO,
    PERFIL_PROFESSOR,
    Usuario,
)

SENHA_PADRAO = os.getenv("SEED_PASSWORD", "Senha@123")

USUARIOS = [
    ("Maria Assistida", "assistido@sgpj.local", PERFIL_ASSISTIDO),
    ("Pedro Aluno", "aluno@sgpj.local", PERFIL_ALUNO),
    ("Ana Professora", "professor@sgpj.local", PERFIL_PROFESSOR),
    ("Carlos Coordenador", "gestao@sgpj.local", PERFIL_GESTAO),
]


def seed_usuarios():
    criados = 0
    for nome, email, perfil in USUARIOS:
        if db.session.scalar(db.select(Usuario).filter_by(email=email)):
            continue
        usuario = Usuario(nome=nome, email=email, perfil=perfil, primeiro_acesso=False)
        usuario.set_senha(SENHA_PADRAO)
        db.session.add(usuario)
        criados += 1
    db.session.commit()
    return criados


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        criados = seed_usuarios()
        print(f"{criados} usuário(s) criado(s). Senha padrão: {SENHA_PADRAO}")
        for _, email, perfil in USUARIOS:
            print(f"  {perfil:<10} {email}")