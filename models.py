from main import db

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relação: Um Evento pode ter muitas Notas Fiscais
    notas = db.relationship('NotaFiscal',backref='evento', lazy=True)

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quem_pagou = db.Column(db.String(100), nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=True) # Caminho do arquivo no servidor

    # Chave Estrangeira: Associa a nota a um Evento
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    