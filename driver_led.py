# ================================================================
# driver_led.py — controle LED via matrice Sense HAT (8x8 RGB)
# Remplace : PCA9685 I2C PWM controller
# (adapté Sense HAT)
# ================================================================
import time
from sense_hat import SenseHat

class DriverLED:
    """Controle la matrice LED 8x8 du Sense HAT.
    
    Simule une LED PWM :
      - luminosite 0-100% ? couleur blanche plus ou moins intense
      - signal_go()       ? clignotement vert pour indiquer GO!
    """

    def __init__(self, channel=0):
        """Initialise le Sense HAT."""
        self.sense = SenseHat()
        self.sense.clear()
        self._luminosite = 0

    def set_luminosite(self, pourcent: int):
        """Regle la luminosite entre 0% (eteint) et 100% (plein blanc)."""
        pourcent = max(0, min(100, pourcent))
        self._luminosite = pourcent
        valeur = int(pourcent / 100 * 255)
        self.sense.clear(valeur, valeur, valeur)  # blanc avec intensite variable

    def allumer(self):
        """Allume toute la matrice en blanc plein."""
        self.set_luminosite(100)

    def eteindre(self):
        """Eteint toute la matrice."""
        self.sense.clear()
        self._luminosite = 0

    def signal_go(self, nb_clignotements=3):
        """Clignote en VERT n fois pour indiquer le signal GO!"""
        for _ in range(nb_clignotements):
            self.sense.clear(0, 200, 0)   # vert
            time.sleep(0.15)
            self.sense.clear()
            time.sleep(0.15)