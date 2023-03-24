from flask import Flask, request, render_template, url_for, redirect, jsonify
import random
import pyrebase
import requests
import json
import time

firebaseConfig = {
  'apiKey': "AIzaSyDFP1OzPFbhsVlxBYBDPrExgH9pB9MGyaI",
  'authDomain': "teste-bot-russ.firebaseapp.com",
  'databaseURL': "https://teste-bot-russ-default-rtdb.firebaseio.com",
  'projectId': "teste-bot-russ",
  'storageBucket': "teste-bot-russ.appspot.com",
  'messagingSenderId': "452650191648",
  'appId': "1:452650191648:web:32a953827982b00919a545",
  'measurementId': "G-8Q1SK4WBK4"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# flask app initializer
app = Flask(__name__)
logged_in_user_id = ''
current_color = None
current_data = None

def login(email, password):
  print("Coloque seus dados de compra!")

  try:
    user = auth.sign_in_with_email_and_password(email, password)
    print("Logado com sucesso!")
  except:
    print("Email ou senha inválidos, tente novamente")
    return False
  return user['idToken']

def generate_colored_numbers():
  global logged_in_user_id
  headers = {"Authorization": f"Bearer {logged_in_user_id}"}
  pegar_dados = requests.get('https://blaze.com/api/roulette_games/recent', headers=headers)
  resultado = json.loads(pegar_dados.content)
  lista_de_numeros = [x['roll'] for x in resultado]
  colored_numbers = []
  for number in lista_de_numeros:
    if number == 0:
      color = "#ffffff"
      text_color = '#000000'
    elif (number > 0 and number < 8):
      color = '#F22C4D'
      text_color = '#ffffff'
    else:
      color = '#000000'
      text_color = '#ffffff'
    
    colored_numbers.append({'num': number, "color": color, "text_color": text_color})
  
  return colored_numbers


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/signin', methods=['POST'])
def signin():
  email = request.form['email']
  password = request.form['password']
  
  if(login(email, password)):
    return redirect(url_for('botscreen', user_id=login(email, password)))
  else:
    return render_template("index.html")
  
  
@app.route('/get_numbers')
def get_numbers():
  global current_data, current_color
  
  cor = random.choice(["#F22C4D", "#000000"])
  
  numbers = generate_colored_numbers()
  if(numbers != current_data):
    current_data = numbers
    current_color = cor
    return jsonify({'data':numbers, 'color':cor})
  else:
    return jsonify({'data': None, 'color': None})

@app.route('/get_numbers')
def get_numbers():
  numbers = generate_colored_numbers() # Assuming func1 returns a list of dicts with 'num', 'color', and 'text_color' keys
  return jsonify(numbers)


@app.route("/botscreen/<user_id>")
def botscreen(user_id):
  global logged_in_user_id
  logged_in_user_id = user_id
  
  cor = random.choice(["#F22C4D", "#000000"])
  return render_template("botscreen.html", output_color=cor, id=user_id, generate_colored_numbers=generate_colored_numbers, numbers=generate_colored_numbers())

  
if __name__ == '__main__':
	app.run(debug=True)


# def gerar_sinal(numero_sorteado):
#   print("Gerando sinal...")

  
#   print(f"Novo número sorteado: {numero_sorteado}")
#   return cor

# lista_de_numeros_anterior = []
# token = login()

# while True:
#   headers = {"Authorization": f"Bearer {token}"}
#   pegar_dados = requests.get('https://blaze.com/api/roulette_games/recent', headers=headers)
#   resultado = json.loads(pegar_dados.content)
#   lista_de_numeros = [x['roll'] for x in resultado]
#   print(lista_de_numeros)
  
#   if lista_de_numeros != lista_de_numeros_anterior:
#     ultimo_numero = lista_de_numeros[-1]
#     gerar_sinal(ultimo_numero)
    
#   lista_de_numeros_anterior = lista_de_numeros
  
#   time.sleep(5)
