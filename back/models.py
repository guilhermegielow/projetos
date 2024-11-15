from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True)
    telefone = db.Column(db.String(15))
    cnpj = db.Column(db.String(15))
    projetos = db.relationship('Projeto', backref='cliente', lazy=True)


class Projeto(db.Model):
    __tablename__ = 'projetos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    atividades = db.relationship('Atividade', backref='projeto', lazy=True)


class Atividade(db.Model):
    __tablename__ = 'atividades'
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())
    projeto_id = db.Column(db.Integer, db.ForeignKey('projetos.id'), nullable=False)


class StatusProjeto(db.Model):
    __tablename__ = 'status_projeto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.Text, nullable=False)
