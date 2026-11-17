from datetime import datetime

from sqlalchemy.orm import validates
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db

PERFIL_ASSISTIDO = "assistido"
PERFIL_ALUNO = "aluno"
PERFIL_PROFESSOR = "professor"
PERFIL_GESTAO = "gestao"

PERFIS = (PERFIL_ASSISTIDO, PERFIL_ALUNO, PERFIL_PROFESSOR, PERFIL_GESTAO)


class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, index=True)  # ver PERFIS
    ativo = db.Column(db.Boolean, nullable=False, default=True)
    primeiro_acesso = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    assistido = db.relationship("Assistido", back_populates="usuario", uselist=False)
    aluno = db.relationship("Aluno", back_populates="usuario", uselist=False)
    professor = db.relationship("Professor", back_populates="usuario", uselist=False)

    @validates("perfil")
    def _validar_perfil(self, _chave, valor):
        if valor not in PERFIS:
            raise ValueError(f"Perfil inválido: {valor!r}. Use um de {PERFIS}.")
        return valor

    @validates("email")
    def _normalizar_email(self, _chave, valor):
        return valor.strip().lower()

    def set_senha(self, senha: str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha: str) -> bool:
        return check_password_hash(self.senha_hash, senha)

    def to_dict(self) -> dict:
        return {
            "id": self.id, "nome": self.nome, "email": self.email,
            "perfil": self.perfil, "primeiro_acesso": self.primeiro_acesso,
        }

    def __repr__(self):
        return f"<Usuario {self.email} ({self.perfil})>"


class Assistido(db.Model):
    __tablename__ = "assistido"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True
    )
    cpf = db.Column(db.String(14), nullable=False, unique=True)
    telefone = db.Column(db.String(20))

    usuario = db.relationship("Usuario", back_populates="assistido")
    atendimentos = db.relationship("Atendimento", back_populates="assistido")
    casos = db.relationship("Caso", back_populates="assistido")


class Aluno(db.Model):
    __tablename__ = "aluno"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True
    )
    matricula = db.Column(db.String(20), nullable=False, unique=True)
    periodo = db.Column(db.Integer)

    usuario = db.relationship("Usuario", back_populates="aluno")
    atendimentos = db.relationship("Atendimento", back_populates="aluno")
    casos = db.relationship("Caso", secondary="caso_aluno", back_populates="alunos")
    atividades = db.relationship("Atividade", back_populates="aluno")


class Professor(db.Model):
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False, unique=True
    )
    matricula = db.Column(db.String(20), nullable=False, unique=True)

    usuario = db.relationship("Usuario", back_populates="professor")
    casos = db.relationship("Caso", back_populates="professor")
    atividades = db.relationship("Atividade", back_populates="professor")