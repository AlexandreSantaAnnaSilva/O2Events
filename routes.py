import os
import config
from main import app, db
from models import Evento, NotaFiscal
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename


def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Rota Principal (Dashboard)
@app.route("/")
def homepage():
    """Exibe a lista de eventos e o dashboard de resumo."""
    eventos = Evento.query.all()

    eventos_com_resumo =[]
    evento = []

    for eventos in eventos:
        total_gasto = sum(nota.valor for nota in eventos.notas)
        #Busca o resumo de quem pagou e quanto
        quem_pagou_lista = db.session.query(
            NotaFiscal.quem_pagou,
            db.func.sum(NotaFiscal.valor)
            ).filter(
                NotaFiscal.evento_id == evento.id
            ).group_by(NotaFiscal.quem_pagou).all()

        eventos_com_resumo.append({
            'evento': evento,
            'total_gasto': float(total_gasto),
            'quem_pagou_resumo': quem_pagou_lista
        })

    return render_template("index.html", eventos_com_resumo=eventos_com_resumo)


# Rota para cadastrar um NOVO EVENTO (GET e POST)
@app.route("/novo_evento", methods=['GET', 'POST'])
def novo_evento():
    """Exibe o formulário de cadastro de evento e processa a submissão."""
    if request.method == 'POST':
        nome_evento = request.form.get('nome_evento').strip()
        
        if not nome_evento:
            flash('O nome do evento não pode ser vazio.', 'warning')
            return redirect(url_for('novo_evento'))
            
        try:
            # Salvar os dados no banco de dados
            novo = Evento(nome=nome_evento)
            db.session.add(novo)
            db.session.commit()
            flash(f'Evento "{nome_evento}" criado com sucesso!', 'success')
            return redirect(url_for('homepage'))
        except Exception as e:
            flash(f'Erro ao criar evento: {e}', 'danger')
            db.session.rollback()

    return render_template("cadastro_evento.html")

# Rota para cadastrar uma nova NOTA FISCAL (GET e POST)
@app.route("/nova_nota", methods=['GET', 'POST'])
def nova_nota():
    """Exibe o formulário de cadastro de nota e processa o upload/submissão."""
    eventos = Evento.query.all()
    
    # Validação para garantir que haja eventos cadastrados
    if not eventos:
        flash('É necessário cadastrar um Evento antes de adicionar uma Nota Fiscal.', 'warning')
        return redirect(url_for('novo_evento'))

    if request.method == 'POST':
        # 1. Processar o upload do arquivo
        arquivo = request.files.get('arquivo_nota')
        caminho_arquivo = None
        
        if arquivo and allowed_file(arquivo.filename):
            filename = secure_filename(arquivo.filename)
            caminho_completo = os.path.join(config.UPLOAD_FOLDER, filename)
            arquivo.save(caminho_completo)
            # Salva o caminho relativo para ser acessível via /files/...
            caminho_arquivo = os.path.join('files', filename) 

        # 2. Salvar os dados no banco de dados
        try:
            # Substitui vírgula por ponto para garantir que float() funcione corretamente
            valor_str = request.form.get('valor').replace(',', '.') 
            
            nova_nf = NotaFiscal(
                descricao=request.form.get('descricao'),
                valor=float(valor_str),
                quem_pagou=request.form.get('quem_pagou'),
                evento_id=int(request.form.get('evento_id')),
                caminho_arquivo=caminho_arquivo
            )
            db.session.add(nova_nf)
            db.session.commit()
            flash('Nota fiscal cadastrada com sucesso!', 'success')
            return redirect(url_for('homepage'))
        except ValueError:
            flash('Erro de formato no valor. Use números e ponto/vírgula para decimais.', 'danger')
            db.session.rollback()
        except Exception as e:
            flash(f'Erro ao cadastrar nota: {e}', 'danger')
            db.session.rollback()

    return render_template("cadastro_nota.html", eventos=eventos)

# Rota para servir arquivos estáticos de upload
@app.route('/files/<filename>')
def uploaded_file(filename):
    """Permite acessar os arquivos de nota fiscal salvos no servidor."""
    # O Flask usa o send_from_directory para servir o arquivo de forma segura
    return send_from_directory(config.UPLOAD_FOLDER, filename)
