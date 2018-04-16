#!/usr/bin/python2

import websocket
import json
import logging
import requests
import threading
import pdb

url = "ws://127.0.0.1/ws"

def loxone(server, DI, state):
    url = "http://{}/dev/sps/io/{}/{}".format(server, DI, state)
    print(url)
    r = requests.get(url)
    print r.status_code

def on_message(ws, message):
    #print message
    obj = json.loads(message)
    if type(obj) == type(dict()):
        obj = [obj]
    for item in obj:
        dev = item.get('dev', 'NA')
        if (dev == 'input'):
            circuit = item.get('circuit', 'NA')
            value = item.get('value', 'NA')
            print("DI!")
            print item
            print("{}/{} = {}".format(dev, circuit, value))
            circuit = 'VI_UP1_DI1.01'
            threading.Thread(target=loxone, kwargs={'server': 'admin:TitkoS12@192.168.88.220', 'DI': circuit, 'state': value}).start()
        elif (dev == 'temp'):
            print("TEMP!")
            print item
            circuit = 'VI_UP1_1W.01'
            value = item.get('value', 'NA')
            threading.Thread(target=loxone, kwargs={'server': 'admin:TitkoS12@192.168.88.220', 'DI': circuit, 'state': value}).start()

def on_error(ws, error):
    print error

def on_close(ws):
    print "Connection closed"


logging.basicConfig(level=logging.DEBUG)
#receiving messages
ws = websocket.WebSocketApp(url, on_message = on_message, on_error = on_error, on_close = on_close)
ws.run_forever()

#sending messages
#ws = websocket.WebSocket()
#ws.connect(url)
#ws.send('{"cmd":"set","dev":"relay","circuit":"3","value":"1"}')
#ws.close()
