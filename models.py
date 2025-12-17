from main import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Evento(db.Model):
    """Modelo para representar um evento (ex: Acamps 2050)."""
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_evento = db.Column(db.DateTime, nullable=True)
    local = db.Column(db.String(200), nullable=True)

    # Relação: Um Evento pode ter muitas Notas Fiscais
    notas = db.relationship('NotaFiscal',backref='evento', lazy='dynamic' , cascade="all, delete-orphan")

    def __repr__(self):
        return f"Evento(id={self.id}, nome='{self.nome}', data_evento='{self.data_evento}')"

class NotaFiscal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    quem_pagou = db.Column(db.String(100), nullable=False)
    caminho_arquivo = db.Column(db.String(255), nullable=True) # Caminho do arquivo no servidor
    data_cadastro = db.Column(db.DateTime, default=datetime.utcnow)

    # Chave Estrangeira: Associa a nota a um Evento
    evento_id = db.Column(db.Integer, db.ForeignKey('evento.id'), nullable=False)
    
    def __repr__(self):
        return f"NotaFiscal(id={self.id}, descricao='{self.descricao}', valor={self.valor})"