# ================================================================
# driver_bp.py — lecture bouton via joystick Sense HAT
# Remplace : expandeur PCF8574 I2C
# Auteur : (adapté Sense HAT)
# ================================================================
import time
import threading
from sense_hat import SenseHat

class DriverBP:
    """Lit le joystick du Sense HAT comme un bouton poussoir.
    
    N'importe quelle direction du joystick (y compris appui central)
    est considérée comme un appui bouton.
    """

    def __init__(self, bit=0):
        """Initialise le Sense HAT."""
        self.sense = SenseHat()
        self._callback = None
        self._running = False
        self._last_state = False

    def est_appuye(self) -> bool:
        """Retourne True si le joystick est actuellement actionné."""
        events = self.sense.stick.get_events()
        for event in events:
            if event.action == 'pressed':
                return True
        return False

    def on_appui(self, callback):
        """Appelle callback(timestamp) a chaque appui du joystick."""
        self._callback = callback
        self._running = True
        threading.Thread(target=self._boucle, daemon=True).start()

    def _boucle(self):
        """Boucle de scrutation à 50 Hz pour détecter les appuis."""
        while self._running:
            events = self.sense.stick.get_events()
            for event in events:
                if event.action == 'pressed':
                    if self._callback:
                        self._callback(time.time())
            time.sleep(0.02)  # 50 Hz

    def arreter(self):
        """Arrete la boucle de scrutation."""
        self._running = False