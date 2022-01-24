import sqlite3

empregados = [
    {"nome":"Bruno", "cargo":"Analista", "salario":2500},
    {"nome":"Gustavo", "cargo":"Desenvolvedor", "salario":3000},
    {"nome":"Luis", "cargo":"Técnico de Integração", "salario":2000},
    {"nome":"Lima", "cargo":"Senior", "salario":3500}
]

conn = sqlite3.connect('cad_dados.db')

cursor = conn.cursor()

for empregado in empregados:
    cursor.execute("""
        INSERT INTO empregados (nome, cargo, salario)
        VALUES (?, ?, ?)
    """, (empregado['nome'], empregado['cargo'], empregado['salario']))

print("Dados inseridos com sucesso!")

conn.commit()
conn.close()