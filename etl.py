import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import sqlite3
import time
import threading
import sys

# Configuration
BROKER_IP = "192.168.141.54"
DUREE_TOURNOI = 10  

heure_debut = 0
scores_tournoi = []

def init_db():
    conn = sqlite3.connect('projet_iot.db')
    conn.execute('DROP TABLE IF EXISTS scores')
    # On ajoute la colonne STATUT pour différencier VALIDE et ELIMINE
    conn.execute('CREATE TABLE scores (id INTEGER PRIMARY KEY AUTOINCREMENT, raspi_id TEXT, score_temps TEXT, statut TEXT)')
    conn.close()

def annoncer_gagnant(client):
    global scores_tournoi, heure_debut
    time.sleep(DUREE_TOURNOI)
    
    # On filtre les survivants (ceux qui n'ont pas fait de faux départ)
    survivants = [s for s in scores_tournoi if s['statut'] == "VALIDE"]
    
    if survivants:
        survivants.sort(key=lambda x: float(x['temps']))
        gagnant = survivants[0]
        msg = f"🏆 VICTOIRE : {gagnant['id']} avec {gagnant['temps']}s"
        client.publish("Jeu/Gagnant", msg)
        print(f"\n{msg}")
    else:
        print("\n⌛ Aucun vainqueur valide pour cette manche.")
    
    client.publish("Jeu/Start", "0")
    heure_debut = 0
    scores_tournoi = []
    print("\n--- Manière terminée. Appuyez sur ENTRÉE pour reset et relancer ---")

def on_message(client, userdata, msg):
    global heure_debut, scores_tournoi
    topic = msg.topic
    
    if "Jeu/" in topic and "/Temps" in topic and heure_debut != 0:
        try:
            payload = msg.payload.decode()
            raspi_id = topic.split('/')[1]
            
            # GESTION DU FAUX DÉPART (-1 envoyé par la Raspi)
            if payload == "-1":
                statut = "ELIMINE"
                affichage = "FAUX DÉPART"
            else:
                statut = "VALIDE"
                affichage = f"{round(float(payload), 4)} s"

            scores_tournoi.append({'id': raspi_id, 'temps': payload, 'statut': statut})
            
            conn = sqlite3.connect('projet_iot.db')
            conn.execute("INSERT INTO scores (raspi_id, score_temps, statut) VALUES (?, ?, ?)", 
                         (raspi_id, affichage, statut))
            conn.commit()
            conn.close()
            print(f"📡 {raspi_id} : {affichage}")
        except:
            pass

# INITIALISATION
init_db()
client = mqtt.Client(CallbackAPIVersion.VERSION2) # Version 2 pour éviter le warning
client.on_connect = lambda c, u, f, rc, p: c.subscribe([("Jeu/Start", 0), ("Jeu/+/Temps", 0)])
client.on_message = on_message

print(f"Connexion à {BROKER_IP}...")
client.connect(BROKER_IP, 1883)

# Thread MQTT
mqtt_thread = threading.Thread(target=client.loop_forever, daemon=True)
mqtt_thread.start()

print("✅ Système prêt ! Appuyez sur ENTRÉE pour démarrer.")

# BOUCLE CLAVIER PRINCIPALE (Évite EOFError)
try:
    while True:
        input() 
        if heure_debut == 0:
            conn = sqlite3.connect('projet_iot.db')
            conn.execute("DELETE FROM scores") # Reset de la page web
            conn.commit()
            conn.close()
            
            heure_debut = time.time()
            client.publish("Jeu/Start", "1")
            print("📢 TOP DÉPART ! (10 secondes)")
            threading.Thread(target=annoncer_gagnant, args=(client,), daemon=True).start()
except (KeyboardInterrupt, EOFError):
    print("\nFermeture...")
    sys.exit()