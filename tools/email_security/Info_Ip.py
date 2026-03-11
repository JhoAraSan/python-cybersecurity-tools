import os
import sys
import requests #pip install requests
import json
from dotenv import load_dotenv #pip install python-dotenv

def ips(API_KEY):
    print("Ingrese las direcciones IP que desea verificar. Presione Enter para finalizar.")
    lista = []
    while True:
        inputs = input()
        if inputs:
            lista.append(inputs)
        else:
            break
    
    for ip in lista:
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}"
        headers = {"Accept": "application/json", "Key": API_KEY}
        response = requests.get(url, headers=headers)
        decodedResponse = json.loads(response.text)
        print (json.dumps(decodedResponse, sort_keys=True, indent=4))

# def ip_isp(ip_check):
#     load_dotenv(dotenv_path="list.env")
#     API_KEY = os.getenv("API_KEY_IPDB")
#     url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip_check}"
#     headers = {"Accept": "application/json", "Key": API_KEY}
#     response = requests.get(url, headers=headers)
#     decodedResponse = json.loads(response.text)
#     return decodedResponse["data"]["isp"]

def network(API_KEY):
    url = 'https://api.abuseipdb.com/api/v2/check-block'
    print("Ingrese la red que desea verificar. Ejemplo: 127.0.0.1/24")
    network = input()
    querystring = {}
    querystring['network'] = network
    querystring['maxAgeInDays'] = '30'
    headers = {
        'Accept': 'application/json'
    }
    headers['Key']=API_KEY

    response = requests.request(method='GET', url=url, headers=headers, params=querystring)

    decodedResponse = json.loads(response.text)
    print (json.dumps(decodedResponse, sort_keys=True, indent=4))

if __name__ == '__main__':
    ENV_PATH = "assets/keys.env"
    try:
        with open(ENV_PATH, 'r') as f:
            pass  # Solo para verificar que el archivo existe
    except FileNotFoundError:
        msn=f"❌ Error: el archivo {ENV_PATH} no se encontró."
        print(msn)
        sys.exit(1)

    load_dotenv(dotenv_path=ENV_PATH)
    API_KEY = os.getenv("API_KEY_IPDB")

    if not API_KEY:
        raise ValueError("Falta la clave API. Defínela en una variable de entorno.")
    
    
    while True:
        try:
            entrada = int(input("\033[31mQue desea hacer?: \033[34m\n1) Validar IP's \n2) Validar Redes \n3) Salir \033[32m\nElija: "))
            match entrada:
                case 1: 
                    ips(API_KEY)
                case 2:
                    network(API_KEY)
                case 3:
                    print("Vemos!!!\nWii\nWii\nWii\nWii")
                    quit()
                case _:
                    print("Seleccion inválida. Inténtalo nuevamente.")
                    continue
        except ValueError:
            print("Entrada inválida. Inténtalo nuevamente.")
        except KeyboardInterrupt:
            print("\n\nComenzemos de Nuevo!\n")
            continue