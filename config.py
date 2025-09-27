import os

# Define o caminho completo para a pasta de upload (static/files)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'files')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

# Garante que a pasta de upload exista. O 'exist_ok=True' evita erro se a pasta já existir.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configurações do Banco de Dados
SQLALCHEMY_DATABASE_URI = 'sqlite:///o2events.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = 'acamps' 
