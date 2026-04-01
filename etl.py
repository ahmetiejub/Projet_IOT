import paho.mqtt.client as mqtt
import sqlite3
import time

# --- CONFIGURATION BASE DE DONNÉES ---
def init_db():
    conn = sqlite3.connect('projet_iot.db')
    cursor = conn.cursor()
    # Création de la table si elle n'existe pas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raspi_id TEXT,
            score_temps REAL,
            date_partie TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# --- LOGIQUE DE SAUVEGARDE (LOAD) ---
def save_score(raspi_id, temps):
    conn = sqlite3.connect('projet_iot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scores (raspi_id, score_temps) VALUES (?, ?)", (raspi_id, temps))
    conn.commit()
    conn.close()
    print(f"Données sauvegardées pour {raspi_id} dans le cylindre !")

# --- LOGIQUE MQTT (EXTRACT & TRANSFORM) ---
def on_message(client, userdata, msg):
    raspi_id = msg.topic.split('/')[-1]
    # On imagine que start_time a été défini au moment du signal START
    delay = round(time.time() - start_time, 3) 
    
    # Appel de la fonction de sauvegarde
    save_score(raspi_id, delay)

# Initialisation
init_db()
# ... reste du code MQTT client.loop_forever()