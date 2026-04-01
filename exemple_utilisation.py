# -*- coding: utf-8 -*-
# ================================================================
# exemple_utilisation.py — exemples d'utilisation des drivers
# Projet IoT — Sense HAT (Raspberry Pi)
# Auteur : Raid Abadou
# ================================================================
# Prerequis :
#   sudo apt install sense-hat -y
# ================================================================

import time
from driver_led import DriverLED
from driver_bp  import DriverBP
from driver_lcd import DriverLCD

# ----------------------------------------------------------------
# 1. LED — matrice 8x8 Sense HAT
# ----------------------------------------------------------------
led = DriverLED()

led.allumer()          # allume en blanc plein (100%)
time.sleep(1)

led.set_luminosite(50) # regle a 50% (blanc moyen)
time.sleep(1)

led.eteindre()         # eteint la matrice
time.sleep(0.5)

led.signal_go()        # clignote 3x en vert -> signal GO!
time.sleep(1)

# ----------------------------------------------------------------
# 2. LCD — texte scrollant sur la matrice
# ----------------------------------------------------------------
lcd = DriverLCD()

lcd.afficher("Bonjour !", "Pret a jouer")   # ligne1 blanc, ligne2 jaune
time.sleep(6)                                # attendre la fin du scroll

lcd.afficher("Score :", "250 ms")
time.sleep(5)

lcd.effacer()          # eteint la matrice
time.sleep(0.5)

# ----------------------------------------------------------------
# 3. Bouton — joystick Sense HAT
# ----------------------------------------------------------------
bp = DriverBP()

print("Appuie sur le joystick (10 secondes)...")

def on_appui(timestamp):
    """Appelee automatiquement a chaque appui du joystick."""
    print(f"  -> Appui detecte ! ts = {timestamp:.3f}")
    led.signal_go(1)                  # 1 clignotement a chaque appui
    lcd.afficher("Appui !", f"{timestamp:.1f}")

bp.on_appui(on_appui)  # enregistre le callback
time.sleep(10)         # ecoute pendant 10 secondes
bp.arreter()           # arrete la scrutation

# ----------------------------------------------------------------
# 4. Exemple combine — mini jeu de reflexe
# ----------------------------------------------------------------
print("\nMini jeu : appuie le plus vite possible apres le signal !")
lcd.afficher("Attention...", "Pret ?")
time.sleep(2)

temps_go = time.time()
led.signal_go()
lcd.afficher("GO !", "Appuie vite !")

appuye = [False]

def on_appui_jeu(timestamp):
    if not appuye[0]:
        appuye[0] = True
        reaction = round((timestamp - temps_go) * 1000)
        print(f"Temps de reaction : {reaction} ms")
        lcd.afficher("Reaction :", f"{reaction} ms")
        led.eteindre()

bp.on_appui(on_appui_jeu)
bp._running = True
import threading
threading.Thread(target=bp._boucle, daemon=True).start()

time.sleep(5)
bp.arreter()
lcd.effacer()
print("Fin de l'exemple.")