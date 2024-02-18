from scipy.sparse import vstack
import gurobipy as gp
import numpy as np
from .lpObject import LPObject
from .lpStateVar import LPStateVar,LPStateVar_zeit,LPStateVar_zusatz
from .lpInputdata import LPInputdata
from scipy.sparse import coo_matrix, csc_matrix, vstack

class LPMain:
    '''
    (Abstrakte) Hauptklasse der linearen Optimierung
    Hier werden die Gleichungssysteme zur Opimierung vorbereitet und die Optimierung durchgeführt
    '''
    def __init__(self,inputdata:LPInputdata):
        if self.__class__.__name__ == 'LPMain':
            raise Exception('Dies ist eine abstrakte Klasse. Bitte nur Objekte der erbenden Klasse erstellen')
        self.Aeq = None
        self.beq = []
        self.senses = []
        self.inputdata = inputdata
        self.make_stateVarLst()
        self.def_pos()
        self.def_bounds()
        self.def_eqs()
        self.init_zielfunktion()
        self.def_zielfunktion()
    
    def def_eqs(self):
        self.obj_lst[0].def_equations()
        self.Aeq,self.beq,self.senses = self.obj_lst[0].return_eqs()
        for obj in self.obj_lst[1:]:
            obj.def_equations()
            self.extend_matrices(obj.return_eqs())
    
    def extend_matrices(self,eq_lst):
        '''Hängt Gleichungen aus anderen Klassen an das Gleichungssystem des LPMain-Objekts an'''
        self.Aeq = vstack([self.Aeq,eq_lst[0]])
        self.beq.extend(eq_lst[1])
        self.senses.extend(eq_lst[2])
    
    def make_stateVarLst(self):
        '''
        Erstellt Listen, die alle Zustandsvariablen aller zum System gehörender Objekte enthält.
        Unterteilt nach zeitabhängigen Variablen und Zusatzvariablen
        '''
        self.stateVars:list[LPStateVar]=[]
        for obj in self.obj_lst:
            self.stateVars.extend(obj.getStateVars())
        # self.stateVars.sort(key=lambda x: x.__class__.__name__) # erst zeit, dann zusatz, da zeit alphabetisch vor zusatz. diese sortierung kann ggf abgeschafft werden, wenn def_pos() anders funktioniert
        self.stateVars_zeitabhg = [var for var in self.stateVars if isinstance(var,LPStateVar_zeit)]
        self.stateVars_zusatz = [var for var in self.stateVars if isinstance(var,LPStateVar_zusatz)]
           
    def def_pos(self):
        '''
        Definiert die Positionen aller Zustandsvariablen in der Aeq-Matrix.
        - Für zeitabhängige Variablen wird die Position der Variable im ersten Zeitschritt gespeichert
        - Zusatzvariablen sind am Ende der Liste
        '''
        idx_pos=0
        for var in self.stateVars_zeitabhg:
            var.pos = idx_pos
            idx_pos += 1
        idx_pos = len(self.stateVars_zeitabhg)*self.inputdata.steps
        for var in self.stateVars_zusatz:
            var.pos = idx_pos
            idx_pos += 1        
        self.inputdata.anz_var=idx_pos #TODO: testen, ob das so jetzt stimmt
        self.inputdata.anz_zeitvar=len(self.stateVars_zeitabhg)

    def def_bounds(self):
        '''
        Erstellt Listen, die die oberen bzw. unteren Grenzen aller Zustandsvariablen enthalten.
        Die Reihenfolge enspricht dabei den Positionen, die den Variablen zugeordnet wurden
        '''
        anz_var_zeitabhg = len(self.stateVars_zeitabhg)*self.inputdata.steps
        anz_var_zusatz = len(self.stateVars_zusatz)
        anz_var = anz_var_zeitabhg + anz_var_zusatz
        self.lb=np.zeros(anz_var)
        self.ub=np.zeros(anz_var)
        
        lb_zeitabhg = []
        ub_zeitabhg = []
        for var in self.stateVars_zeitabhg:
            lb_zeitabhg.append(var.lb)   
            ub_zeitabhg.append(var.ub)   
        self.lb[0:anz_var_zeitabhg] = lb_zeitabhg*self.inputdata.steps
        self.ub[0:anz_var_zeitabhg] = ub_zeitabhg*self.inputdata.steps
                
        lb_zusatz=[]
        ub_zusatz=[]
        for var in self.stateVars_zusatz:
            lb_zusatz.append(var.lb)
            ub_zusatz.append(var.ub)
        self.lb[anz_var_zeitabhg:] = lb_zusatz
        self.ub[anz_var_zeitabhg:] = ub_zusatz
        
    def init_zielfunktion(self):
        '''Initialisierung der Zielfunktionen mit einem Nullvektor'''
        self.f = np.zeros(self.inputdata.anz_var)
    
    def def_zielfunktion(self):
        pass
    
    def add_var_zielfunktion(self,var:LPStateVar,step,value):# TODO funktioniert so noch nicht mit Zusatzvariablen
        '''
        Fügt eine Variable der Zielfunktion hinzu
        Dazu muss die StateVar, der gewünschte Zeitschritt und die Gewichtung für die Zielfunktion übergeben werden
        '''
        self.f[var.pos+step*len(self.stateVars_zeitabhg)]=value
        
    def optimize(self):
        '''Führt die lineare Optimierung des aufgestellten Gleichungssystems aus'''
        x=self.solver_gurobi()
        self.ergebnis_zuweisen(x)
    
    def ergebnis_zuweisen(self,x):
        '''Weist die Ergebnisse des Ergebnisvektors x den Zustandsvariablen zu'''
        self.x = x
        anz_zeitVars = len(self.stateVars_zeitabhg)
        for var in self.stateVars_zeitabhg:
            var.result = x[:anz_zeitVars*self.inputdata.steps][var.pos::anz_zeitVars]
        for var in self.stateVars_zusatz:
            var.result = x[var.pos]
    
# %% Funktion Solver
    def solver_gurobi(self):
        '''Die Funktion solver_gurobi übergibt das Optimierungsmodell an den Gurobi-Solver, führt die Optimierung durch und gibt das Ergebnis zurück.
        Aeq, beq, senses: Matriz bzw. Vektor der Gleichungen mit dem Vergleichsoperator jeder Gleichung
        ctype, lb, ub: Typ sowie obere und untere Grenze der Variablen
        f: Zielfunktion'''
        # Übergabe des Optimierungsproblems an die Gurobi API.
        # leeres Problem anlegen
        problem = gp.Model()
        # Variablen
        x = problem.addMVar(shape=self.inputdata.anz_var,lb=self.lb,ub=self.ub,vtype=['C' for _ in range(self.inputdata.anz_var)])
        # Zielfunktion übergeben
        problem.setObjective(self.f @ x, gp.GRB.MINIMIZE)    
        # Gleichungen übergeben
        problem.addMConstr(self.Aeq.tocsr(), x, self.senses, self.beq)
        # Problem optimieren bzw. lösen
        problem.setParam('MIPGap', 0.00)  # prozentuale Entfernung zur optimalen Lösung
        problem.optimize()
        x = x.X
        return x