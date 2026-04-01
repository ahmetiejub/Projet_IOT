# client.py
import json, time, cwiid
import paho.mqtt.client as mqtt
from config     import *
from driver_bp  import DriverBP
from driver_led import DriverLED

print('Appuyez sur 1+2 sur la Wiimote...')
try:
    wm = cwiid.Wiimote()
    wm.rpt_mode = cwiid.RPT_NUNCHUK | cwiid.RPT_BTN
    print('Wiimote connectee !')
except RuntimeError:
    print('ERREUR : Wiimote introuvable.')
    exit(1)

bp     = DriverBP(bit=0)
led    = DriverLED(channel=1)
en_jeu = False

def lire_luminosite() -> int:
    state = wm.state
    if 'nunchuk' not in state:
        return -1
    x = state['nunchuk']['stick'][cwiid.X] - 128
    y = state['nunchuk']['stick'][cwiid.Y] - 128
    amplitude = max(abs(x), abs(y))
    if amplitude < STICK_THRESHOLD:
        return -1
    return int(amplitude / 128 * 100)

def on_appui_bouton(timestamp):
    global en_jeu
    if not en_jeu:
        print('Faux depart !')
        client.publish(TOPIC_ANSWER, json.dumps({'ts': timestamp, 'faux': True}))
    else:
        print(f'Appui a t={timestamp:.3f}')
        client.publish(TOPIC_ANSWER, json.dumps({'ts': timestamp, 'faux': False}))
        led.eteindre()
        en_jeu = False

def on_message(client, userdata, msg):
    global en_jeu
    if msg.topic == TOPIC_GO:
        print('GO ! Appuyez !')
        en_jeu = True
        led.allumer()
    elif msg.topic == TOPIC_RESULT:
        data = json.loads(msg.payload)
        if 'ms' in data:
            print(f"Votre temps : {data['ms']} ms")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connecte au broker MQTT SSL')
        client.subscribe([(TOPIC_GO, 0), (TOPIC_RESULT, 0)])

client = mqtt.Client()
client.tls_set(ca_certs=CA_CERT)
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER_HOST, BROKER_PORT)
client.loop_start()

bp.on_appui(on_appui_bouton)

print('Pret. Stick = lumiere | Bouton = reflexe')
while True:
    pourcent = lire_luminosite()
    if pourcent >= 0:
        client.publish(TOPIC_LIGHT, str(pourcent))
    time.sleep(0.1)
