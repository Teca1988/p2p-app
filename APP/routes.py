from flask import Blueprint, request, redirect, url_for, session, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from APP import db
from functools import wraps
from datetime import datetime

# Criação do blueprint para as rotas
routes_bp = Blueprint('routes', __name__)

# Modelos do banco de dados
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    account_balance = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class TransactionModel(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

# Decorador para proteger rotas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota principal
@routes_bp.route('/')
@routes_bp.route('/index')
def index():
    return "O Flask está funcionando!"

# Rota para exibir usuários
@routes_bp.route('/users')
@login_required
def show_users():
    users = UserModel.query.all()
    return render_template('users.html', users=users)

# Rota para transferências
@routes_bp.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    message = None
    if request.method == 'POST':
        sender_id = request.form.get('sender_id')
        receiver_id = request.form.get('receiver_id')
        amount = float(request.form.get('amount'))

        sender = UserModel.query.get(sender_id)
        receiver = UserModel.query.get(receiver_id)

        if not sender or not receiver:
            message = "Remetente ou destinatário não encontrados!"
        elif sender_id == receiver_id:
            message = "O remetente e o destinatário não podem ser os mesmos!"
        elif sender.account_balance < amount:
            message = "Saldo insuficiente!"
        else:
            sender.account_balance -= amount
            receiver.account_balance += amount
            db.session.add(TransactionModel(sender_id=sender.id, receiver_id=receiver.id, amount=amount))
            db.session.commit()
            message = "Transferência realizada com sucesso!"

    users = UserModel.query.all()
    return render_template('transfer.html', users=users, message=message)

# Rota para exibir transações
@routes_bp.route('/transactions')
@login_required
def show_transactions():
    transactions = TransactionModel.query.all()
    return render_template('transactions.html', transactions=transactions)

# Rota de login
@routes_bp.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = UserModel.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('routes.transfer'))
        else:
            message = "Email ou senha inválidos!"

    return render_template('login.html', message=message)

# Rota de logout
@routes_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('routes.login'))

