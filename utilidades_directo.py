from re import *
from numpy import *

class Central():
    def __init__(self, signo, arbol, operador, posicion, verificador):
        self.posicion0 = []
        self.ultimaposicion = []
        self.signo = signo
        self.arbol = arbol
        self.operador = operador
        self.posicion = posicion
        self.verificador = verificador

        if self.signo in "E":
            self.is_nulla = True
        self.asignacion_orden()
            
    #Asignacion de first y last positions
    def asignacion_orden(self):
        if self.operador:
            if self.signo == "|":
                self.posicion0 = self.posicion[0].posicion0 + self.posicion[1].posicion0
                self.ultimaposicion = self.posicion[0].ultimaposicion + self.posicion[1].ultimaposicion

            elif self.signo == "-":
                if self.posicion[0].verificador:
                    self.posicion0 = self.posicion[0].posicion0 + self.posicion[1].posicion0
                else:
                    self.posicion0 = self.posicion[0].posicion0
                
                if self.posicion[1].verificador:
                    self.ultimaposicion = self.posicion[0].ultimaposicion + self.posicion[1].ultimaposicion
                else:
                    self.ultimaposicion = self.posicion[1].ultimaposicion
            
            elif self.signo == "*":
                self.posicion0 = self.posicion[0].posicion0
                self.ultimaposicion = self.posicion[0].ultimaposicion

        else:
            if self.signo not in "E":
                self.posicion0.append(self.arbol)
                self.ultimaposicion.append(self.arbol)





        




        




