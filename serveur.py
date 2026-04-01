import time
import os
from paho.mqtt import client as mqtt_client

# --- PARAMÈTRES SERVEUR ---
BROKER = 'localhost'
PORT = 1883
CLIENT_ID = 'Serveur_Maitre_Du_Jeu'

TOPIC_START = "Jeu/Start"
TOPIC_GAGNANT = "Jeu/Gagnant"
TOPIC_ECOUTE_TEMPS = "Jeu/+/Temps" 

scores = {} 
jeu_en_cours = False
historique = [] 

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Serveur Prêt et connecté à Mosquitto !")
            client.subscribe(TOPIC_ECOUTE_TEMPS)
        else:
            print("❌ Erreur de connexion")

    def on_message(client, userdata, msg):
        global scores, jeu_en_cours
        if not jeu_en_cours:
            return 

        topic_parts = msg.topic.split('/')
        if len(topic_parts) == 3:
            joueur_id = topic_parts[1]
            temps_str = msg.payload.decode("utf-8")
            try:
                temps = float(temps_str)
                # ANTI-TRICHE : Faux départ si le temps est sous 0.1s
                if temps < 0.1:
                    print(f"⚠️ FAUX DÉPART ! {joueur_id} a anticipé (Temps : {temps}s) -> Score ignoré.")
                else:
                    scores[joueur_id] = temps
                    print(f"⏱️ REÇU : {joueur_id} a réagi en {temps} secondes !")
            except ValueError:
                pass

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    return client

def afficher_historique():
    print("\n" + "="*40)
    print("📜 HISTORIQUE DES PARTIES ")
    if len(historique) == 0:
        print("Aucune partie n'a encore été jouée.")
    else:
        for partie in historique:
            print(f"Manche {partie['manche']} | Gagnant : {partie['gagnant']} ({partie['temps']}s)")
    print("="*40 + "\n")

def run():
    global scores, jeu_en_cours, historique
    client = connect_mqtt()
    client.loop_start()

    while True:
        print("\n" + "-"*30)
        print("🎮 MENU DU MAÎTRE DU JEU 🎮")
        print("1. Lancer une nouvelle manche")
        print("2. Voir l'historique des parties")
        print("3. Quitter le serveur")
        print("-"*30)
        
        choix = input("Votre choix (1, 2 ou 3) : ")

        if choix == '1':
            scores = {} 
            jeu_en_cours = True

            print("\n DÉPART : Envoi du signal '1'...")
            client.publish(TOPIC_START, "1")

            print(" Attente des réactions (5 secondes)...")
            time.sleep(5)

            jeu_en_cours = False
            print("\n FIN : Envoi du signal '0'...")
            client.publish(TOPIC_START, "0")

            if scores:
                gagnant = min(scores, key=scores.get)
                meilleur_temps = scores[gagnant]
                print(f"\n LE GAGNANT EST : {gagnant} avec {meilleur_temps}s ! ")
                client.publish(TOPIC_GAGNANT, gagnant)
                
                # Mise à jour de l'historique en mémoire
                historique.append({
                    'manche': len(historique) + 1,
                    'gagnant': gagnant,
                    'temps': meilleur_temps
                })
                
                #  SAUVEGARDE EN DUR DANS UN FICHIER TEXTE
                with open("historique_scores.txt", "a", encoding="utf-8") as fichier:
                    fichier.write(f"Manche {len(historique)} | Gagnant : {gagnant} ({meilleur_temps}s)\n")
                print(" Score sauvegardé dans 'historique_scores.txt'")
                
            else:
                print("\n Aucun joueur n'a réagi à temps (ou faux départs uniquement).")
                client.publish(TOPIC_GAGNANT, "Personne")
                
        elif choix == '2':
            afficher_historique()
            
        elif choix == '3':
            print("Arrêt du serveur.")
            break
            
        else:
            print("Choix invalide, veuillez taper 1, 2 ou 3.")

    client.loop_stop()

if __name__ == '__main__':
    run()