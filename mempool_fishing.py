from websocket import create_connection
import json
import time
import ssl
import websocket

fortuna_address = 'addr1wynelppvx0hdjp2tnc78pnt28veznqjecf9h3wy4edqajxsg7hwsc'
lord_tuna = '279f842c33eed9054b9e3c70cd6a3b32298259c24b78b895cb41d91a'
#Acquire outside infinite loop
ws = create_connection("ws://<your-ogmios-ip>:1337")
#ws = websocket.WebSocket(sslopt={"cert_reqs": ssl.CERT_NONE})
#ws.connect('wss://<ogmios-https-endpoint>/')
xinit = True
datum = 'Old'
#loop through requesting NextT
while True:
    if xinit:
        xinit = False
        wsend = ws.send('{ "type": "jsonwsp/request", "version": "1.0", "servicename": "ogmios", "methodname": "AwaitAcquire", "args": {} }')
        aacq = ws.recv()
        ares = json.loads(aacq)
    if ares['result'] is not None:
        wsend = ws.send('{ "type": "jsonwsp/request", "version": "1.0", "servicename": "ogmios", "methodname": "NextTx", "args": {"fields": "all"} }')
        og = ws.recv()
        ogres = json.loads(og)
        if ogres['result'] == None:
            #break
            wsend = ws.send('{ "type": "jsonwsp/request", "version": "1.0", "servicename": "ogmios", "methodname": "ReleaseMempool", "args": {"fields": "all"} }')
            time.sleep(2)
            og = ws.recv()
            ogres = json.loads(og)
            wsend = ws.send('{ "type": "jsonwsp/request", "version": "1.0", "servicename": "ogmios", "methodname": "AwaitAcquire", "args": {} }')
            aacq = ws.recv()
            ares = json.loads(aacq)
        else:
            for n in ogres['result']['body']['outputs']:
                txhash = ogres['result']['id']
                inputs = ogres['result']['body']['inputs']
                outputs = ogres['result']['body']['outputs']
                if n['address'] == fortuna_address:
                    if n['datum'] != datum:
                        datum = n['datum']
                        print('New Datum!')
                        print('TxHash -',txhash)
                        print(inputs)
                        print(n['datum'])
                        f = open("tuna_datum.txt", "w")
                        f.write(n['datum'])
                        f.close()
                        f = open("tuna_hash.txt", "w")
                        f.write(txhash)
                        f.close()
                        f = open("tuna_coins.txt", "w")
                        f.write(str(n['value']['coins']))
                        f.close()
                    break
