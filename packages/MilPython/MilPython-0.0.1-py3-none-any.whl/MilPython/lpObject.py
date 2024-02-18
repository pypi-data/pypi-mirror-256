import numpy as np
from .lpStateVar import LPStateVar, LPStateVar_zeit,LPStateVar_zusatz
from .lpInputdata import LPInputdata
from scipy.sparse import coo_matrix, csc_matrix
from .equation import Equation as Eq

class LPObject:
    def __init__(self,inputdata:LPInputdata,name:str,comment:str):
        '''Konstruktor des allgemeinen Linear Programming Objects'''
        if self.__class__.__name__ == 'LPObject':
            raise Exception('Dies ist eine abstrakte Klasse. Bitte nur Objekte der erbenden Klasse erstellen')
        self.inputdata = inputdata
        self.name = name
        self.comment = comment
        self.stateVar_lst:list[LPStateVar]=[]
        self.eq_lst=[]

    def add_time_var(self,name,unit='',lb=0,ub=np.inf,comment='')->LPStateVar_zeit:
        var = LPStateVar_zeit(name,unit,lb,ub,comment)
        self.stateVar_lst.append(var)
        return var
    
    def add_additional_var(self,name,unit='',lb=0,ub=np.inf,comment='')->LPStateVar_zusatz:
        var = LPStateVar_zusatz(name,unit,lb,ub,comment)
        self.stateVar_lst.append(var)
        return var
    
    def add_eq(self,var_lst,sense='E',b=0):
        self.eq_lst.append(Eq(var_lst,sense,b))
    
    def getStateVars(self)->list[LPStateVar]:
        '''gibt die Liste der Zustandsvariablen zurück'''
        return self.stateVar_lst
                
    def def_equations(self):
        # raise Exception('This method must be overritten by the inheriting class.')
        pass
    
    def return_eqs(self):
        # Bestimmung anz_var
        anz_var = sum(len(eq.var_lst) for eq in self.eq_lst)
        self.idx=0
        self.eq_nr=0
        self.row = np.zeros(shape=(anz_var,))
        self.col = np.zeros(shape=(anz_var,))
        self.data = np.zeros(shape=(anz_var,))
        self.senses=[]
        self.beq = []
        
        for eq in self.eq_lst:
            for var in eq.var_lst: 
                if len(var) == 2: #TODO Überprüfung, ob das viel Rechenzeit kostet: Alternative
                    var.append(0)
                self.row[self.idx] = self.eq_nr
                self.col[self.idx] = var[0].pos + var[2] * self.inputdata.anz_zeitvar
                self.data[self.idx] = var[1]
                self.idx+=1
            self.senses.append(eq.sense)
            self.beq.append(eq.b)
            self.eq_nr+=1
        Aeq_temp = coo_matrix((self.data,(self.row,self.col)),shape=(self.eq_nr,self.inputdata.anz_var))
        return Aeq_temp,self.beq,self.senses   
