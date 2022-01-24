from flask import Flask, request, Response, g
import sqlite3

app = Flask(__name__)

DB_URL = "cad_dados.db"

users = [
    {"username":"burno", "secret":"1234"}
]

@app.before_request
def before_request():
    print("Conectando ao banco")
    conn = sqlite3.connect(DB_URL)
    g.conn = conn

@app.teardown_request
def after_request(exception):
    if g.conn is not None:
        g.conn.close()
        print("Desconectando do banco!")

def query_employers_to_dict(conn, query):
    cursor = conn.cursor()
    cursor = g.conn.execute(query)
    employers_dict = [{'nome':row[0], 'cargo':row[1], 'salario':row[2]}
        for row in cursor.fetchall()]
    return employers_dict

def check_user(username, secret):
    for user in users:
        if (user["username"] == username) and (user["secret"] == secret):
            return True
    return False

@app.route('/')
def home():
    return "<h1>Olá, café!</h1>"

@app.route('/empregados')
def get_empregados():

    query = """
        SELECT nome, cargo, salario
        FROM empregados;
    """

    employers_dict = query_employers_to_dict(g.conn, query)

    print(employers_dict)

    return {'empregados': employers_dict}

@app.route('/empregados/<cargo>')
def get_empregados_cargo(cargo):
    query = f"""
        SELECT nome, cargo, salario
        FROM empregados
        WHERE "cargo" LIKE "{cargo}"
    """

    employers_dict = query_employers_to_dict(g.conn, query)

    return {'empregados': employers_dict}

@app.route('/empregados/<info>/<value>')
def get_empregados_info(info, value):

    if value.isnumeric():
        value = float(value)

    query = f"""
        SELECT nome, cargo, salario
        FROM empregados
        WHERE "{info}" LIKE "{value}"
    """

    employers_dict = query_employers_to_dict(g.conn, query)

    return {'empregados': employers_dict}

@app.route('/informations', methods=['POST'])
def get_empregados_post():

    username = request.form['username']
    secret = request.form['secret']

    if not check_user(username, secret):
        return Response("Unauthorized", status=401)

    info = request.form['info']
    value = request.form['value']

    if value.isnumeric():
        value = float(value)

    query = f"""
        SELECT nome, cargo, salario
        FROM empregados
        WHERE "{info}" LIKE "{value}"
    """

    employers_dict = query_employers_to_dict(g.conn, query)

    return {'empregados': employers_dict}       

@app.route('/register', methods=['POST'])
def add_empregados_post():

    username = request.form['username']
    secret = request.form['secret']

    if not check_user(username, secret):
        return Response("Unauthorized", status=401)
    
    nome = request.form['nome']
    cargo = request.form['cargo']
    salario = request.form['salario']

    query = f"""
        INSERT INTO empregados (nome, cargo, salario)
        VALUES ("{nome}", "{cargo}", "{salario}")
    """

    cursor = g.conn.cursor()
    cursor.execute(query)

    g.conn.commit()

    return {'empregados': "Registered employee"}    

if __name__ == '__main__':
    app.run(debug=True)