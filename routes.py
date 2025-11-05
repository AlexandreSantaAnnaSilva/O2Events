import os
import config
from main import app, db
from models import Evento, NotaFiscal
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound 


def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Rota Principal (Dashboard)
@app.route("/")
def homepage():
    """Exibe a lista de eventos e o dashboard de resumo."""

    # 1. Busca todos os eventos ( return uma lista de objetos Evento)
    todos_eventos = Evento.query.all()

    eventos_com_resumo =[]

    # 2. Itera sobre CADA evento individualmente. 'evento_obj' e o objeto que tem o .id
    for evento_obj in todos_eventos:
        # Calcula o total gasto
        total_gasto = sum(nota.valor for nota in evento_obj.notas)
        
        # Busca o resumo de quem pagou e quanto
        quem_pagou_lista = db.session.query(
            NotaFiscal.quem_pagou,
            db.func.sum(NotaFiscal.valor)
            ).filter(
                NotaFiscal.evento_id == evento_obj.id
            ).group_by(NotaFiscal.quem_pagou).all()

        eventos_com_resumo.append({
            'evento': evento_obj,
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
            
            # Garante que a pasta de upload exista
            os.makedirs(config.UPLOAD_FOLDER, exist_ok=True) 
            
            arquivo.save(caminho_completo)
            
            # CORREÇÃO CRÍTICA: Salva no DB APENAS o nome do arquivo.
            # A rota de download (uploaded_file) usará o UPLOAD_FOLDER + este nome.
            caminho_arquivo = filename 

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
    """Permite acessar os arquivos de nota fiscal salvos no servidor e força o download."""
    try:
        # send_from_directory usa config.UPLOAD_FOLDER como diretório base e 'filename' como o arquivo a ser buscado.
        return send_from_directory(config.UPLOAD_FOLDER, filename, as_attachment=True)
    except NotFound:
        # Se o arquivo não for encontrado no diretório, redireciona com mensagem de erro.
        flash(f"O arquivo {filename} não foi encontrado no servidor.", 'danger')
        return redirect(url_for('homepage'))

# -----------------------------------------------------------
#  ROTAS DE EXCLUSÃO E DETALHES
# -----------------------------------------------------------

@app.route("/detalhes_evento/<int:evento_id>")
def detalhes_evento(evento_id):
    """Exibe os detalhes de um evento específico e suas notas fiscais."""
    evento = Evento.query.get_or_404(evento_id)
    
    # Busca todas as notas fiscais do evento
    notas = NotaFiscal.query.filter_by(evento_id=evento_id).order_by(NotaFiscal.id.desc()).all()
    
    # Calcula o total gasto
    total_gasto = sum(nota.valor for nota in notas)
    
    return render_template("detalhes_evento.html", evento=evento, notas=notas, total_gasto=float(total_gasto))

@app.route("/excluir_evento/<int:evento_id>", methods=['POST'])
def excluir_evento(evento_id):
    """Exclui um evento e todas as suas notas fiscais associadas."""
    evento = Evento.query.get_or_404(evento_id)
    
    # 1. Processa a exclusão de arquivos e notas fiscais
    try:
        nome_evento = evento.nome
        
        # Deleta os arquivos físicos das notas antes de deletar as entradas no DB
        for nota in evento.notas:
            if nota.caminho_arquivo:
                caminho_completo = os.path.join(config.UPLOAD_FOLDER, nota.caminho_arquivo)
                if os.path.exists(caminho_completo):
                    os.remove(caminho_completo)
        
        # 2. Exclui o evento e suas notas fiscais relacionadas (graças ao relacionamento)
        db.session.delete(evento)
        db.session.commit()
        flash(f'Evento "{nome_evento}" e todas as suas notas fiscais foram excluídos com sucesso!', 'success')
        return redirect(url_for('homepage'))
    except Exception as e:
        flash(f'Erro ao excluir evento: {e}', 'danger')
        db.session.rollback()
        return redirect(url_for('homepage'))

@app.route("/excluir_nota/<int:nota_id>", methods=['POST'])
def excluir_nota(nota_id):
    """Exclui uma nota fiscal específica e seu arquivo físico, se existir."""
    nota = NotaFiscal.query.get_or_404(nota_id)
    
    # Salva o ID do evento para redirecionamento
    evento_id = nota.evento_id
    descricao_nota = nota.descricao

    # 1. Processa a exclusão do arquivo físico
    try:
        if nota.caminho_arquivo:
            caminho_completo = os.path.join(config.UPLOAD_FOLDER, nota.caminho_arquivo)
            if os.path.exists(caminho_completo):
                os.remove(caminho_completo)
        
        # 2. Exclui a entrada no banco de dados
        db.session.delete(nota)
        db.session.commit()
        
        flash(f'Nota Fiscal "{descricao_nota}" excluída com sucesso!', 'success')
        
        # Redireciona para a página de detalhes do evento
        return redirect(url_for('detalhes_evento', evento_id=evento_id))
        
    except Exception as e:
        flash(f'Erro ao excluir nota fiscal: {e}', 'danger')
        db.session.rollback()
        # Se falhar, tenta voltar para os detalhes, ou para o dashboard
        try:
             return redirect(url_for('detalhes_evento', evento_id=evento_id))
        except:
             return redirect(url_for('homepage'))
