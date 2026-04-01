# Projet IoT : Guide de connexion pour l'Équipe Terrain (Clients)

Le Serveur Central MQTT est maintenant configuré et prêt à recevoir les données de vos capteurs.

Voici comment connecter vos Raspberry Pi (ou vos PC) à mon serveur.

## 1. Prérequis
Vous avez uniquement besoin d'installer la librairie Python pour communiquer en MQTT.
Dans votre terminal, tapez :
`pip install paho-mqtt`

*(Note : Ne lancez pas de serveur Mosquitto de votre côté, c'est mon PC qui gère tout).*

## 2. Configuration de votre script
Ouvrez votre fichier client (`client-mqtt.py`). 
Remplacez la variable `BROKER = 'localhost'` par mon adresse IP sur le réseau de l'école :

`BROKER = '192.168.141.54'`

## 3. Les Topics (Canaux) MQTT à utiliser
Pour que nos scripts se comprennent, utilisez ces canaux :

* **Sens Serveur -> Client (Écouter le départ du jeu) :** Abonnez-vous à `Jeu/Start`.
* **Sens Client -> Serveur (Envoyer vos actions) :** Publiez vos messages (appui bouton, Nunchuk) sur le topic `Jeu/Action/Equipe1` (remplacez "Equipe1" par votre identifiant).

## 4. Lancement !
1. Assurez-vous d'être branchés sur le même réseau que moi (filaire ou Wi-Fi de l'école).
2. Lancez votre script : `python client-mqtt.py`
3. Envoyez un message, il s'affichera directement sur mon terminal !