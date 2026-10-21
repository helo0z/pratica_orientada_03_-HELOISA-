from database import db

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    # Relacionamento 1:N com livros
    books = db.relationship('Book', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.nome}>"

# Modelo de Livro
class Book(db.Model):
    __tablename__ = 'livros'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    
    # Chave estrangeira ligando ao usuario
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    def __repr__(self):
        return f"<Book {self.titulo}>"