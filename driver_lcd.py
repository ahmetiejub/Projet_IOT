# -*- coding: utf-8 -*-
import threading
from sense_hat import SenseHat

class DriverLCD:
    def __init__(self):
        self.sense = SenseHat()
        self.sense.clear()
        self._thread = None

    def afficher(self, ligne1='', ligne2=''):
        def _scroll():
            if ligne1.strip():
                self.sense.show_message(
                    ligne1.strip(),
                    scroll_speed=0.06,
                    text_colour=[255, 255, 255]
                )
            if ligne2.strip():
                self.sense.show_message(
                    ligne2.strip(),
                    scroll_speed=0.06,
                    text_colour=[255, 220, 0]
                )
        self._thread = threading.Thread(target=_scroll, daemon=True)
        self._thread.start()

    def effacer(self):
        self.sense.clear()
