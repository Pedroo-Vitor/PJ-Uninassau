from datetime import date, datetime

from ..extensions import db

SITUACOES_CASO = ("em_andamento", "pendente", "encerrado")
STATUS_ATIVIDADE = ("pendente", "entregue", "validada", "revisao")

caso_aluno = db.Table(
    "caso_aluno",
    db.Column("caso_id", db.Integer, db.ForeignKey("caso.id"), primary_key=True),
    db.Column("aluno_id", db.Integer, db.ForeignKey("aluno.id"), primary_key=True),
)


class Atendimento(db.Model):
    __tablename__ = "atendimento"

    id = db.Column(db.Integer, primary_key=True)
    assistido_id = db.Column(
        db.Integer, db.ForeignKey("assistido.id"), nullable=False, index=True
    )
    aluno_id = db.Column(
        db.Integer, db.ForeignKey("aluno.id"), nullable=False, index=True
    )
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descricao = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    assistido = db.relationship("Assistido", back_populates="atendimentos")
    aluno = db.relationship("Aluno", back_populates="atendimentos")
    caso = db.relationship("Caso", back_populates="atendimento", uselist=False)
    documentos = db.relationship("Documento", back_populates="atendimento")


class Caso(db.Model):
    __tablename__ = "caso"

    id = db.Column(db.Integer, primary_key=True)
    # Um atendimento origina no máximo um caso.
    atendimento_id = db.Column(
        db.Integer, db.ForeignKey("atendimento.id"), unique=True
    )
    assistido_id = db.Column(
        db.Integer, db.ForeignKey("assistido.id"), nullable=False, index=True
    )
    # Associado depois da abertura (RN-03), por isso opcional.
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"), index=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    area = db.Column(db.String(60))
    situacao = db.Column(
        db.String(20), nullable=False, default="em_andamento", index=True
    )  # ver SITUACOES_CASO
    data_abertura = db.Column(db.Date, nullable=False, default=date.today)
    data_encerramento = db.Column(db.Date)

    atendimento = db.relationship("Atendimento", back_populates="caso")
    assistido = db.relationship("Assistido", back_populates="casos")
    professor = db.relationship("Professor", back_populates="casos")
    alunos = db.relationship("Aluno", secondary=caso_aluno, back_populates="casos")
    atividades = db.relationship("Atividade", back_populates="caso")
    prazos = db.relationship("Prazo", back_populates="caso")
    documentos = db.relationship("Documento", back_populates="caso")
    orientacoes = db.relationship("Orientacao", back_populates="caso")
    historico = db.relationship("Historico", back_populates="caso")


class Atividade(db.Model):
    __tablename__ = "atividade"

    id = db.Column(db.Integer, primary_key=True)
    caso_id = db.Column(
        db.Integer, db.ForeignKey("caso.id"), nullable=False, index=True
    )
    aluno_id = db.Column(
        db.Integer, db.ForeignKey("aluno.id"), nullable=False, index=True
    )
    professor_id = db.Column(db.Integer, db.ForeignKey("professor.id"))
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(
        db.String(20), nullable=False, default="pendente", index=True
    )  # ver STATUS_ATIVIDADE
    resposta = db.Column(db.Text)
    prazo = db.Column(db.Date)
    entregue_em = db.Column(db.DateTime)
    validada_em = db.Column(db.DateTime)

    caso = db.relationship("Caso", back_populates="atividades")
    aluno = db.relationship("Aluno", back_populates="atividades")
    professor = db.relationship("Professor", back_populates="atividades")
    prazos = db.relationship("Prazo", back_populates="atividade")


class Prazo(db.Model):
    __tablename__ = "prazo"

    id = db.Column(db.Integer, primary_key=True)
    caso_id = db.Column(
        db.Integer, db.ForeignKey("caso.id"), nullable=False, index=True
    )
    atividade_id = db.Column(db.Integer, db.ForeignKey("atividade.id"))
    descricao = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False, index=True)
    concluido = db.Column(db.Boolean, nullable=False, default=False)

    caso = db.relationship("Caso", back_populates="prazos")
    atividade = db.relationship("Atividade", back_populates="prazos")


class Documento(db.Model):
    __tablename__ = "documento"

    id = db.Column(db.Integer, primary_key=True)
    caso_id = db.Column(db.Integer, db.ForeignKey("caso.id"), index=True)
    atendimento_id = db.Column(db.Integer, db.ForeignKey("atendimento.id"))
    enviado_por_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    nome_original = db.Column(db.String(255), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)
    tipo_mime = db.Column(db.String(100))
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    caso = db.relationship("Caso", back_populates="documentos")
    atendimento = db.relationship("Atendimento", back_populates="documentos")
    enviado_por = db.relationship("Usuario")


class Orientacao(db.Model):
    __tablename__ = "orientacao"

    id = db.Column(db.Integer, primary_key=True)
    caso_id = db.Column(
        db.Integer, db.ForeignKey("caso.id"), nullable=False, index=True
    )
    professor_id = db.Column(
        db.Integer, db.ForeignKey("professor.id"), nullable=False
    )
    texto = db.Column(db.Text, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    caso = db.relationship("Caso", back_populates="orientacoes")
    professor = db.relationship("Professor")


class Historico(db.Model):
    """Rastreabilidade (RF11 / RN-06): quem fez o quê, quando e em qual caso."""

    __tablename__ = "historico"

    id = db.Column(db.Integer, primary_key=True)
    caso_id = db.Column(db.Integer, db.ForeignKey("caso.id"), index=True)
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )
    acao = db.Column(db.String(60), nullable=False)
    descricao = db.Column(db.String(255))
    criado_em = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, index=True
    )

    caso = db.relationship("Caso", back_populates="historico")
    usuario = db.relationship("Usuario")