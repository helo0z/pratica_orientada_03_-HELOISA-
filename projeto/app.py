import os
from flask import Flask, render_template, request, redirect, url_for
from database import db
from models import User, Book

app = Flask(__name__)

# Configura o banco SQLite local na mesma pasta
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'biblioteca.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas se ainda nao existirem
with app.app_context():
    db.create_all()

# Rota principal - lista usuarios e livros
@app.route('/')
def index():
    usuarios = User.query.all()
    livros = Book.query.all()
    return render_template('index.html', usuarios=usuarios, livros=livros)

# Rota GET/POST para cadastro de usuario
@app.route('/usuarios/novo', methods=['GET', 'POST'])
def novo_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        # Validação simples
        if not nome or not email:
            return "Por favor preencha todos os campos!", 400

        novo_user = User(nome=nome, email=email)
        db.session.add(novo_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('user_form.html')

# Rota GET/POST para cadastro de livro
@app.route('/livros/novo', methods=['GET', 'POST'])
def novo_livro():
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        user_id = request.form.get('user_id')

        if not titulo or not user_id:
            return "Preencha o titulo e selecione um usuario!", 400

        novo_book = Book(titulo=titulo, user_id=int(user_id))
        db.session.add(novo_book)
        db.session.commit()

        return redirect(url_for('index'))

    # Pega usuarios para preencher o <select> no formulario
    usuarios = User.query.all()
    return render_template('book_form.html', usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)