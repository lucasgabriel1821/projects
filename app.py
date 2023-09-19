from flask import Flask, request, render_template, redirect, url_for
import pymysql
import yagmail

app = Flask(__name__)

DB_HOST = "******"
DB_USER = "******"
DB_PASSWORD = "******"
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

def obter_itens_do_banco():
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT nome, quantidade FROM estoque")
    resultados = cursor.fetchall()
    itens = [
        {"nome": nome, "quantidade": quantidade} for nome, quantidade in resultados
    ]
    conn.close()
    return itens

def enviar_email_com_lista(estoque, destinatario_email):
    remetente_email = "email@email.com"
    remetente_senha = "******"

    yag = yagmail.SMTP(remetente_email, remetente_senha)

    email_body = "<html><body><table>"
    email_body += "<tr><th>Nome</th><th>Quantidade</th></tr>"
    for item in estoque:
        email_body += f"<tr><td>{item['nome']}</td><td>{item['quantidade']}</td></tr>"
    email_body += "</table></body></html>"

    try:
        yag.send(to=destinatario_email, subject="Relação de Estoque", contents=email_body)
        yag.close()
        return "E-mail enviado com sucesso."
    except Exception as e:
        return f"Erro ao enviar o e-mail: {str(e)}"

@app.route("/enviar_email", methods=["POST"])
def enviar_email():
    destinatario_email = request.form.get("email")

    estoque = obter_itens_do_banco()

    resultado = enviar_email_com_lista(estoque, destinatario_email)

    return resultado

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

@app.route("/editar/<string:nome>", methods=["GET", "POST"])
def editar_item(nome):
    conn = pymysql.connect(
        host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM estoque WHERE nome = %s", (nome,))
    item = cursor.fetchone()

    novo_nome = request.form.get("novo_nome", "")
    nova_quantidade = request.form.get("nova_quantidade", "")

    if request.method == "POST":
        novo_nome = request.form.get("novo_nome", None)
        nova_quantidade = request.form.get("nova_quantidade", None)

        if novo_nome:
            cursor.execute(
                "UPDATE estoque SET nome = %s WHERE nome = %s", (novo_nome, nome)
            )

        if nova_quantidade:
            cursor.execute(
                "UPDATE estoque SET quantidade = %s WHERE nome = %s",
                (nova_quantidade, nome),
            )

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("editar.html", item=item)

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
