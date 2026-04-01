# config.py

# -- Réseau MQTT --------------------------------------------------
BROKER_HOST = '192.168.141.54'   # <-- mets l'IP de ton serveur ici
BROKER_PORT = 1883
CA_CERT     = 'ca.crt'         # certificat SSL

# -- Topics MQTT --------------------------------------------------
TOPIC_GO     = 'Jeu/Start'
TOPIC_ANSWER = 'game/answer'
TOPIC_RESULT = 'game/result'
TOPIC_LIGHT  = 'light/cmd'

# -- Adresses I2C -------------------------------------------------
I2C_ADDR_LED = 0x40    # PCA9685
I2C_ADDR_BP  = 0x20    # PCF8574
I2C_ADDR_LCD = 0x27    # LCD 16x2

# -- Nunchuk ------------------------------------------------------
STICK_THRESHOLD = 60   # zone morte du stick