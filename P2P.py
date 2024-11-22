from flask_migrate import Migrate
from APP import create_app, db  # Importa a factory function e o banco de dados

app = create_app()  # Criação da aplicação Flask a partir da factory function
app.secret_key = 'sua_chave_super_secreta'
migrate = Migrate(app, db)  # Configura o Flask-Migrate

if __name__ == "__main__":
    app.run(debug=True)  # Inicia o servidor no modo debug