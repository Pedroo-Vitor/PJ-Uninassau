from datetime import datetime

from ..extensions import db

PERFIS = ("assistido", "aluno", "professor", "gestao")


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