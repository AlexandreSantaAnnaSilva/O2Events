from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config # Importa as configurações do arquivo config.py

app = Flask(__name__)
app.config.from_object(config)

db = SQLAlchemy(app)

# IMPORTAÇÃO DA ROTAS

from routes import *
from models import *

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
