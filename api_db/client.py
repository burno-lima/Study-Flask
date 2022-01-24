from flask import request
import requests

response = requests.get('http://127.0.0.1:5000/empregados')

# data = {"username":"burno", "secret":"1234", "cargo":"Engenheiro", "nome":"Pedro", "salario":"6500"}
# response = requests.post('http://127.0.0.1:5000/register', data=data)

if response.status_code == 200:
    message = response.json()
    print(message['empregados'])
else:
    print(response.status_code)