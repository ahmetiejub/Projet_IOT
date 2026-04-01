# server.py
import json, time, random
import paho.mqtt.client as mqtt
from config     import *
from driver_lcd import DriverLCD
from driver_led import DriverLED

lcd      = DriverLCD()
led      = DriverLED(channel=0)
temps_go = None

def lancer_tour():
    global temps_go
    delai = round(random.uniform(1.0, 5.0), 1)
    lcd.afficher('Attention...', f'Signal dans {delai}s')
    time.sleep(delai)
    temps_go = time.time()
    led.signal_go()
    client.publish(TOPIC_GO, json.dumps({'ts': temps_go}))
    lcd.afficher('  --- GO! ---', 'Appuyez vite !')

def on_message(client, userdata, msg):
    global temps_go
    if msg.topic == TOPIC_ANSWER and temps_go is not None:
        data  = json.loads(msg.payload)
        faux  = data.get('faux', False)
        if faux:
            lcd.afficher('Faux depart !', 'Recommence...')
            client.publish(TOPIC_RESULT, json.dumps({'erreur': 'faux_depart'}))
        else:
            latence = round((data['ts'] - temps_go) * 1000)
            print(f'Temps de reaction : {latence} ms')
            lcd.afficher('Reaction :', f'  {latence} ms')
            client.publish(TOPIC_RESULT, json.dumps({'ms': latence}))
        temps_go = None
        time.sleep(3)
        lancer_tour()
    elif msg.topic == TOPIC_LIGHT:
        pourcent = int(msg.payload)
        led.set_luminosite(pourcent)
        lcd.afficher('Luminosite :', f'  {pourcent} %')

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connecte au broker MQTT SSL')
        client.subscribe([(TOPIC_ANSWER, 0), (TOPIC_LIGHT, 0)])
    else:
        print(f'Erreur connexion : code {rc}')

client = mqtt.Client()
client.tls_set(ca_certs=CA_CERT)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT)

lcd.afficher('Serveur pret', 'Connexion...')
time.sleep(1)
lancer_tour()
client.loop_forever()