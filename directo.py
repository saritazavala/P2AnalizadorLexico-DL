from utilidades_directo import *
from funciones_trans import *
from AnalizadorLexico import *

#AnalizadorLexico = analizador
alpha = "abcdefghijklmnopqrstuvwxyz0123456789E#"
class Directo:
    def __init__(self, expresion):
        self.estados = []
        self.estado0 = None
        self.estadoF = None
        self.estdosAceptacion = []
        self.transiciones = []
        self.alpha = []

        self.nombre = 0
        self.n_utilizados = 0
        self.arbol = 0
        self.nodos = []
        self.posiciones = {}
        self.epicentro = None

        regular_exp_mod = transform_exp(expresion, 2)
        regular_exp_mod = add_concat(regular_exp_mod)
        self.create_sintx_tree(regular_exp_mod)

        for x in self.nodos:
            if x.signo == '#':
                self.estadoF = x.arbol
                break

        self.get_all_follow_pos()
        self.create()

    def set_name(self):
        possible_names = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
        name = possible_names[self.nombre]
        self.nombre += 1

        if self.nombre == len(possible_names):
            self.n_utilizados += 1
            self.nombre = 0
        return name + str(self.n_utilizados)

    def get_precedence_of_two(self, first, second):
        pre_fir = precedencia_op(first)
        pre_sec = precedencia_op(second)
        return pre_fir >= pre_sec


   
    def create_sintx_tree(self, expresion):
        caracteres = []
        operadores = []

      
        for i in expresion:
            if i in alpha:
                caracteres.append(i)

        
            elif i == "(":
                operadores.append(i)

            elif i == ")":
                caracter_final = operadores[-1] if operadores else None
                while caracter_final is not None and caracter_final[0] != "(":
                    epi = self.get_operations(operadores, caracteres)
                    caracteres.append(epi)
                    caracter_final = operadores[-1] if operadores else None
                operadores.pop()

            else:
                caracter_final = operadores[-1] if operadores else None
                while caracter_final is not None and caracter_final not in "()" and self.get_precedence_of_two(caracter_final, i):
                    epi = self.get_operations(operadores, caracteres)
                    caracteres.append(epi)
                    caracter_final = operadores[-1] if operadores else None
                operadores.append(i)


        final = self.get_operations(operadores, caracteres)
        caracteres.append(final)
        self.epicentro = caracteres.pop()


    def get_operations(self, operadores, caracteres):
        op = operadores.pop()
        derecha = caracteres.pop()
        izquierda = None

       
        if (derecha not in self.alpha) and (derecha != "E") and (derecha !=  "#") and (derecha is not None):
            self.alpha.append(derecha)
        

        if op != "*":
            izquierda = caracteres.pop()
            if (izquierda not in self.alpha) and (izquierda != "E") and (izquierda !=  "#") and (izquierda is not None):
                self.alpha.append(izquierda)

       
        if op == "|" or op == "-": return self.orAndOperation(izquierda, derecha, op)
        elif op == "*": return self.kleenOperation(derecha)


   
    def orAndOperation(self, izquierdo, derecho, operador):
        
        if (type(izquierdo) == Central) and (type(derecho) == Central):
            if operador == "|":
                fuente = Central(operador, None, True, [izquierdo, derecho], izquierdo.verificador or derecho.verificador)
                self.nodos += [fuente]
                return fuente
            elif operador == "-":
                fuente = Central(operador, None, True, [izquierdo, derecho], izquierdo.verificador and derecho.verificador)
                self.nodos += [fuente]
                return fuente

        
        elif (type(izquierdo) != Central) and (type(derecho) != Central):
            if operador == "|":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "E" else None
                etiqueta_derecha = self.arbol + 2  if derecho not in "E" else None
                self.arbol = self.arbol + 2
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, nodo_derecho], nodo_izquierdo.verificador or nodo_derecho.verificador)
                self.nodos += [nodo_izquierdo, nodo_derecho, fuente]
                return fuente
            elif operador == "-":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "E" else None
                etiqueta_derecha = self.arbol + 2  if derecho not in "E" else None
                self.arbol = self.arbol + 2
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, nodo_derecho], nodo_izquierdo.verificador and nodo_derecho.verificador)
                self.nodos += [nodo_izquierdo, nodo_derecho, fuente]
                return fuente

       
        elif (type(izquierdo) == Central) and (type(derecho) != Central):
            if operador == "|":
                etiqueta_derecha = self.arbol + 1  if derecho not in "E" else None
                self.arbol = self.arbol + 1
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [izquierdo, nodo_derecho], izquierdo.verificador or nodo_derecho.verificador)
                self.nodos += [nodo_derecho, fuente]
                return fuente
            elif operador == "-":
                etiqueta_derecha = self.arbol + 1  if derecho not in "E" else None
                self.arbol = self.arbol + 1
                nodo_derecho = Central(derecho, etiqueta_derecha, False, [], False)
                fuente = Central(operador, None, True, [izquierdo, nodo_derecho], izquierdo.verificador and nodo_derecho.verificador)
                self.nodos += [nodo_derecho, fuente]
                return fuente

       
        elif (type(izquierdo) != Central) and (type(derecho) == Central):
            if operador == "|":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "E" else None
                self.arbol = self.arbol + 1
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                fuente = Central(operador   , None, True, [nodo_izquierdo, derecho], nodo_izquierdo.verificador or derecho.verificador)
                self.nodos += [nodo_izquierdo, fuente]
                return fuente

            elif operador == "-":
                etiqueta_izquierda = self.arbol + 1  if izquierdo not in "E" else None
                self.arbol = self.arbol + 1
                nodo_izquierdo = Central(izquierdo, etiqueta_izquierda, False, [], False)
                fuente = Central(operador, None, True, [nodo_izquierdo, derecho], nodo_izquierdo.verificador and derecho.verificador)
                self.nodos += [nodo_izquierdo, fuente]
                return fuente


    def kleenOperation(self, nodo_hijo):
       
        if (type(nodo_hijo) == Central):
            fuente_interrogacion = Central("*", None, True, [nodo_hijo], True)
            self.nodos += [fuente_interrogacion]
            return fuente_interrogacion
        # Caso el nodo hijo no exista
        else:
            identificador = self.arbol + 1 if nodo_hijo not in "E" else None
            self.arbol = self.arbol + 1
            var_nodo_hijo = Central(nodo_hijo, identificador, False, [], False)
            fuente_interrogacion = Central("*", None, True, [var_nodo_hijo], True)
            self.nodos += [var_nodo_hijo, fuente_interrogacion]
            return fuente_interrogacion


   
    def get_all_follow_pos(self):
        for x in self.nodos:
            if not x.operador and not x.verificador:
                self.set_follow_pos(x.arbol, [])

            if x.signo == "-":
                primer_hijo = x.posicion[0]
                segundo_hijo = x.posicion[1]

                for y in primer_hijo.ultimaposicion:
                    self.set_follow_pos(y, segundo_hijo.posicion0)

            if x.signo == "*":
                for y in x.ultimaposicion:
                    self.set_follow_pos(y, x.posicion0)


    def set_follow_pos(self, arbol, posicion_siguiente):
        if arbol not in self.posiciones.keys():
            self.posiciones[arbol] = []

        self.posiciones[arbol] += posicion_siguiente
        self.posiciones[arbol] = set_to_list(self.posiciones[arbol])

    def get_node_by_id(self, arbol):
        for x in self.nodos:
            if x.arbol == arbol:
                return x


    def create(self):
        estado_inicial = self.epicentro.posicion0
        nodo_estado_inicial = afd_node(self.set_name(), estado_inicial, 2)
        self.estados.append(nodo_estado_inicial)
        self.estado0 = nodo_estado_inicial.signo

       
        if self.estadoF in [x for x in nodo_estado_inicial.nodos]:
            self.estdosAceptacion.append(nodo_estado_inicial.signo)

       
        estados_etiquetados = [estado.terminado for estado in self.estados]
        while False in estados_etiquetados:
            
            for estado in self.estados:
                if not estado.terminado:
                    estados_sin_etiqeutar = estado
                    break
            estados_sin_etiqeutar.terminado = True
            
            
            for s in self.alpha:
                if type(s) != Central:
                    siguiente_pos_entry = []
                    for x in estados_sin_etiqeutar.nodos:
                        if self.get_node_by_id(x).signo == s:
                            siguiente_pos_entry += self.posiciones [x]
                    siguiente_pos_entry = set_to_list(siguiente_pos_entry)
                    
                    if siguiente_pos_entry is empty:
                        continue
                    nuevo = afd_node(self.set_name(), siguiente_pos_entry, 2)

                    
                    if nuevo.estados not in [estado.estados for estado in self.estados] and nuevo.estados != "":
                        if self.estadoF in [nodo for nodo in nuevo.nodos]:
                            self.estdosAceptacion .append(nuevo.signo)
                        self.estados.append(nuevo)
                        self.transiciones.append([estados_sin_etiqeutar.signo, s, nuevo.signo])
                    
                    else:
                        self.nombre -= 1
                        for estado in self.estados:
                            if nuevo.estados == estado.estados:
                                self.transiciones.append([estados_sin_etiqeutar.signo, s, estado.signo])
                            
            estados_etiquetados = [estado.terminado for estado in self.estados]









        

        