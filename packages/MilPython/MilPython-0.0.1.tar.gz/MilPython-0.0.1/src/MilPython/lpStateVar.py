import matplotlib.pyplot as plt

class LPStateVar:
    '''
    Abstrakte Klasse (nur Objekte der erbenden Klassen erstellen)
    Definiert Zustandsvariablen für die lineare Optimierung
    beinhaltet Name, Einheut, lower und upper bound und Platz für Kommentare
    beim Optimieren werden unter self.result die optimierten Ergebnisse für die Variable abgelegt
    '''
    def __init__(self,name,unit=None,lb=0,ub=float('inf'),comment=None):
        if self.__class__.__name__ == 'LPStateVar':
            raise Exception('Diese Klasse ist abstrakt und dient nicht der Instanzierung. Bitte Objekte der erbenden Klassen zeit oder zusatz erstellen')
        self.pos:int=None
        self.name:str=name
        self.lb:float=lb
        self.ub:float=ub
        self.unit:str=unit
        self.result = None
        self.comment:str=comment
    
    def __repr__(self):
        return f"StateVar(name='{self.name}')"
    
class LPStateVar_zeit(LPStateVar):
    '''
    Klasse für zeitabhängige Zustandsvariablen
    Es wird automatisch eine Variable dieses Typs für jeden Zeitschritt angelegt
    self.pos entspricht der Position der Variable in Zeitschritt null.
    '''
    def __init__(self, name, unit=None,  lb=0, ub=float('inf'), comment=None):
        super().__init__(name, unit, lb, ub, comment)
    
    def plot_result(self):
        '''Einfache Methode zum Plotten der Zeitveräufe des Optimierungsergebnisses für diese Variable'''
        if self.result is None:
            print('Es muss zunächst die Optimierung durchgeführt werden')
            return
        plt.plot(self.result)
        plt.title(self.name)
        plt.ylabel(self.unit)
        plt.xlabel('steps')
        plt.show()
    
    def __repr__(self):
        if self.result is not None:
            self.plot_result()
        return f"StateVar(name='{self.name}')"

class LPStateVar_zusatz(LPStateVar):
    '''Klasse für Zusatzvariablen, die nur einfach (und nciht in jedem Zeitschritt) auftreten'''
    def __init__(self, name, unit=None, lb=0, ub=float('inf'), comment=None):
        super().__init__(name, unit, lb, ub, comment)