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
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)

def getList():

    global userKey
    userKey = str(input("Sartu zure API key \n"))

    metodoa = 'GET'
    uria = "https://api.thingspeak.com/channels.json?api_key="+userKey
    erantzuna= requests.request(metodoa, uria, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    lista = json.loads(erantzuna.content)
    i = 0
    if len(lista)>0:
        channelKeys = [None] * len(lista)
        id = [None] * len(lista)
        for x in lista:
            id[i] = x['id']
            channelKeys[i] = x['api_keys'][0]['api_key']
            i += 1
        print(str(len(id)) + " kanal daude, zein erabili nahi duzu?")
        for j in id:
            print(j)
        aukera = int(input("Sartu aukera \n"))

        global channelKey
        global channelId
        channelId = str(id[aukera - 1])
        channelKey = str(channelKeys[aukera - 1])
    else:
        create()
    cpu_ram()

def create():
    metodoa = 'POST'
    uria = "https://api.thingspeak.com/channels.json"
    goiburuak = {'Host': 'api.thingspeak.com', 'Content-Type': 'application/x-www-form-urlencoded'}
    edukia = {'api_key': userKey, 'name' : 'myChannel', 'field1' : 'CPU', 'field2' : 'RAM'}
    edukia_encoded = urllib.parse.urlencode(edukia)
    goiburuak['Content-Length'] = str(len(edukia_encoded))
    erantzuna = requests.request(metodoa, uria, data=edukia_encoded, headers=goiburuak, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)
    edukia = erantzuna.content
    print(edukia)
    gauzak = json.loads(erantzuna.content)
    global channelId
    global channelKey
    channelId = str(gauzak['id'])
    channelKey = str(gauzak['api_keys'][0]['api_key'])

def handler(sig_num, frame):
    print('\nSignal handler called with signal ' + str(sig_num))
    clear()
    print('\nExiting gracefully')
    sys.exit(0)


def igo(cpu, ram):
    metodoa = 'GET'
    uria = "https://api.thingspeak.com/update?api_key="+channelKey+"&field1="+str(cpu)+"&field2="+str(ram)
    erantzuna= requests.request(metodoa, uria, allow_redirects=False)
    kodea = erantzuna.status_code
    deskribapena = erantzuna.reason
    print(str(kodea) + " " + deskribapena)

def cpu_ram():
    while True:

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        print("CPU: %" + str(cpu) + "\tRAM: %" + str(ram))
        igo(cpu, ram)
        time.sleep(15)

if __name__ == "__main__":


    signal.signal(signal.SIGINT, handler)
    getList()

