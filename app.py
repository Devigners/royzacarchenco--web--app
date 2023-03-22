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

def login():
  while True:
    print("Coloque seus dados de compra!")
    email = input("Email: ")
    password = input("Senha: ")

    try:
      user = auth.sign_in_with_email_and_password(email, password)
      print("Logado com sucesso!")
      break
    except:
      print("Email ou senha inválidos, tente novamente")

  return user['idToken']

def gerar_sinal(numero_sorteado):
  print("Gerando sinal...")
  cor = random.choice(["vermelho", "preto"])
  print(f"Cor: {cor}")
  
  print(f"Novo número sorteado: {numero_sorteado}")
  # sua lógica para indicar uma entrada
  # ...

  return cor

lista_de_numeros_anterior = []
token = login()

while True:
  headers = {"Authorization": f"Bearer {token}"}
  pegar_dados = requests.get('https://blaze.com/api/roulette_games/recent', headers=headers)
  resultado = json.loads(pegar_dados.content)
  lista_de_numeros = [x['roll'] for x in resultado]
  print(lista_de_numeros)
  
  if lista_de_numeros != lista_de_numeros_anterior:
    ultimo_numero = lista_de_numeros[-1]
    gerar_sinal(ultimo_numero)
    
  lista_de_numeros_anterior = lista_de_numeros
  
  time.sleep(5)
