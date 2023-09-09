from flask import Flask, request, render_template, redirect, url_for, session
import pymysql

app = Flask(__name__)

DB_HOST = "127.0.0.1"
DB_USER = "root"
DB_PASSWORD = "28491@Lucas"
DB_NAME = "estoque"

def create_table():
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS estoque (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            quantidade INT NOT NULL
        )
    """
    )
    conn.commit()
    conn.close()


create_table()


@app.route("/")
def index():
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade FROM estoque")
    estoque = cursor.fetchall()
    conn.close()
    return render_template("index.html", estoque=estoque)


@app.route("/adicionar", methods=["GET", "POST"])
def adicionar_item():
    if request.method == "POST":
        nome = request.form["nome"]
        quantidade = request.form["quantidade"]
        conn = pymysql.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO estoque (nome, quantidade) VALUES (%s, %s)", (nome, quantidade)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("adicionar.html")


@app.route('/editar/<string:nome>', methods=['GET', 'POST'])
def editar_item(nome):
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM estoque WHERE nome = %s', (nome,))
    item = cursor.fetchone()

    if request.method == 'POST':
        if 'novo_nome' in request.form:
            novo_nome = request.form['novo_nome']
            if novo_nome:
                cursor.execute('UPDATE estoque SET nome = %s WHERE nome = %s', (novo_nome, nome))
        if 'nova_quantidade' in request.form:
            nova_quantidade = request.form['nova_quantidade']
            if nova_quantidade:
                cursor.execute('UPDATE estoque SET quantidade = %s WHERE nome = %s', (nova_quantidade, nome))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('editar.html', item=item)

@app.route("/excluir/<string:nome>")
def excluir_item(nome):
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estoque WHERE nome = %s", (nome,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
