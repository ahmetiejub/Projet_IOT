#!/usr/bin/python3
import random
from paho.mqtt import client as mqtt_client
import time


# Adresse et port du serveur MQTT
BROKER = '192.168.141.54'
PORT = 1883

client_id = f"{random.randint(0, 10000)}"

TOPICS = {"Start":"Jeu/Start", "Gagnant":"Jeu/Gagnant" , "Temps": f"Jeu/{client_id}/Temps" }



# Se connecter au brocker et récupérer l'objet Client
def connect_mqtt(broker, port) -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            subscribe(client)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client

def jeu(client):
	attente = random.randint(1, 5)
	print("allumage des LEDs rouges")
	time.sleep(attente)
	
	time_start = time.monotonic()
	print("allumage des LEDs vertes / start timer")
	input()
	time_end = time.monotonic()
	
	delai = time_end - time_start
	
	print(f"delai = {delai}")
	send_message(client, TOPICS["Temps"], delai)


# Fonction pour s'abonner à tous les topics (variable TOPICS)
def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        content = msg.payload.decode()
        print(f"[{msg.topic}] Received `{content}`")

        if msg.topic == "Jeu/Start":
            if content == "1":
                print("Début du jeu")
                jeu(client)
                # Allumage des LEDs, Timer....

            elif content == "0":
                print("Fin du jeu")
                # Extinction des LEDs, reset des timers...
    
        if msg.topic == "Jeu/Gagnant":
            print(f"[{msg.topic}] Gagnant reçu: {content}")
            # Vérifier si le gagnant reçu est soi-même

    
    client.subscribe(TOPICS["Start"])
    client.subscribe(TOPICS["Gagnant"])
    client.on_message = on_message


# Fonction pour envoyer un message sur un topic
def send_message(client, topic, message):
    result = client.publish(topic, message)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"[{topic}] Send `{message}`")
    else:
        print(f"[{topic}] Failed to send message")


def run():
    client = connect_mqtt(BROKER, PORT)
    client.loop_forever()

if __name__ == '__main__':
    run()
