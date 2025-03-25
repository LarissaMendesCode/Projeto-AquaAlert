from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = "chave_secreta"  # chave para usar flash messages

# Configuração do banco de dados
def init_sqlite_db():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_sqlite_db()  # Inicializa o banco de dados

# Rota para o formulário de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Criptografa a senha
        password_hash = generate_password_hash(password)

        # Salva no banco de dados
        try:
            conn = sqlite3.connect('usuarios.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
            conn.commit()
            conn.close()
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Erro: Nome de usuário já existe!', 'error')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

# Rota para o formulário de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica o nome de usuário e a senha no banco de dados
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            flash('Login realizado com sucesso!', 'success')
            session['username'] = username  # Armazena o usuário na sessão
            return redirect(url_for('dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# Rota para a página inicial após o login
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return f"Bem-vindo, {session['username']}! Esta é sua página inicial."
    else:
        flash('Por favor, faça login primeiro.', 'error')
        return redirect(url_for('login'))

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Você saiu com sucesso.', 'success')
    return redirect(url_for('login'))


# Rota inicial
@app.route('/')
def index():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)