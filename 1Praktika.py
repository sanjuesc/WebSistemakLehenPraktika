import signal
import sys
import urllib

import requests
import psutil
import time
import json

userKey = ''
channelId= ''
channelKey= ''

def clear():
    metodoa = 'DELETE'
    uria = "https://api.thingspeak.com/channels/"+channelId+"/feeds.json"
    goiburuak = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': userKey}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    if kodea == 200:
        print("Kanala ondo garbitu da")
    else:
        print("Kanala ez da garbitu, lortutako errorea hurrengoa da")
        print(str(kodea) + " " + deskribapena)

def hasi():
    global userKey
    global channelKey
    global channelId
    lista_lortuta = False

    while lista_lortuta == False:
        userKey = str(input("Sartu zure API key \n"))
        metodoa = 'GET'
        uria = "https://api.thingspeak.com/channels.json?api_key=" + userKey
        erantzuna = requests.request(metodoa, uria, allow_redirects=False)
        kodea = erantzuna.status_code
        if kodea == 200:
            lista_lortuta=True
        else:
            print("API key-a ez da zuzena")
    deskribapena = erantzuna.reason
    lista = json.loads(erantzuna.content)
    i = 0
    if len(lista)>0:
        channelKeys = [None] * len(lista)
        print(str(len(lista)) + " kanal daude, zein erabili nahi duzu? (1,2,3 edo 4 sartu)")
        id = [None] * len(lista)
        for x in lista:
            id[i] = x['id']
            channelKeys[i] = x['api_keys'][0]['api_key']
            print(x['name'])
            i += 1
        aukera = int(input("Sartu aukera \n"))
        channelId = str(id[aukera - 1])
        channelKey = str(channelKeys[aukera - 1])
    else:
        print("Ez dituzu kanalik oraindik, beraz, berri bat sortuko dugu")
        create()
    cpu_ram()

def create():
    global channelId
    global channelKey
    izena = str(input("Sartu sortu nahi duzun kanalaren izena\n"))
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': userKey, 'name': izena, 'field1': 'CPU', 'field2': 'RAM'}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    if kodea == 200:
        print("Kanala ondo sortu da")
        gauzak = json.loads(erantzuna.content)
        channelId = str(gauzak['id'])
        channelKey = str(gauzak['api_keys'][0]['api_key'])
    else:
        print("Kanala ez da sortu, lortutako errorea hurrengoa da")
        print(str(kodea) + " " + deskribapena)
        sys.exit(0)


def handler(sig_num, frame):
    print('\nSignal handler called with signal ' + str(sig_num))
    clear()
    sys.exit(0)


def igo(cpu, ram):
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update?api_key="+channelKey+"&field1="+str(cpu)+"&field2="+str(ram)
    erantzuna= requests.request(metodoa, uria, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    if kodea == 200:
        print("Informazioa ondo igo da")
    else:
        print("Informazioa ez da igo, lortutako errorea hurrengoa da")
        print(str(kodea) + " " + deskribapena)

def cpu_ram():
    while True:

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        print("Uneko erabilera: CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        igo(cpu, ram)
        time.sleep(15)

if __name__ == "__main__":


    signal.signal(signal.SIGINT, handler)
    hasi()

