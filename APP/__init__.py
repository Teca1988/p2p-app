from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Configuração do banco de dados
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configurações do Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'sua_chave_super_secreta'  # Chave secreta para sessões

    # Inicializa o banco de dados com o app Flask
    db.init_app(app)

    # Registra o blueprint
    from APP.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
