class LPInputdata:
    '''
    Klasse, die alle Eingangsdaten für die lineare Optimierung enthält.
    Beinhaltet die Zeitreihen als Dict
    In der Initialisierung des LPMain-Objekts wird dieser Klasse außerdem die Gesamtanzahl an Variablen zugewiesen
    '''
    def __init__(self,data,dt_h):
        self.data = data                            # dict mit Zeitreihen
        self.steps=len(next(iter(data.items()))[1]) # Anzahl der steps = länge der ersten liste im input-dict
        self.dt_h = dt_h                            # Schrittgröße in Stunden
        self.anz_var=None