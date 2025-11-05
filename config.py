import os

# Definição do diretório base
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define o caminho completo para a pasta de upload dentro de 'static'
# A função nativa do Flask (baseada em os.path.join) é mais robusta,
# mas esta definição direta é a mais clara para o ambiente.
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Configurações do Banco de Dados
SQLALCHEMY_DATABASE_URI = 'sqlite:///o2events.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'acamps'

# Garante que a pasta de upload exista. O 'exist_ok=True' evita erro se a pasta já existir.
# MANTEMOS A CHAMADA DE CRIAÇÃO DE PASTA NO PRÓPRIO config.py
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
