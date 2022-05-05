
from AnalizadorLexico import *
from Estado import *
import copy
from transicion import *
from AFN import *
#from subconjuntos import *
from operator import attrgetter
import graphviz 

class Thompson:
    def __init__(self, expresion_regular):
        self.a = AnalizadorLexico(expresion_regular)
        self.maquinas = []
        self.expresion_regular = self.a.convertir_postfix()

    def parsing(self):
        alpha = self.a.alfabeto(self.expresion_regular)
        #print(alpha)
        for i in self.expresion_regular:
            if i == "*":
                self.asterisco(self.maquinas.pop())
            if i in alpha:
                self.paso_base(i)
            if i == "+":
                self.plus(self.maquinas.pop())
            if i == "|":
                self.OR(self.maquinas.pop(),self.maquinas.pop())
            if i == "?":
                self.interrogacion(self.maquinas.pop())
            if i == ".":
                self.concatenacion(self.maquinas.pop(),self.maquinas.pop())

        return self.maquinas[0]
        
        
    
    def compilar(self):
        
        # print(self.maquinas)
        # self.paso_base("a") 
        # self.paso_base("b") 
        # # self.asterisco(self.maquinas.pop())
        # # self.paso_base("b")
        # # self.asterisco(self.maquinas.pop())
        # # self.concatenacion(self.maquinas.pop(), self.maquinas.pop())
        # # print(self.maquinas)
        # # self.graficar()
        # #self.plus(self.maquinas.pop())
        # self.OR(self.maquinas.pop(), self.maquinas.pop() )
        # self.paso_base("c")
        # self.concatenacion(self.maquinas.pop(), self.maquinas.pop())
        # # self.paso_base("c") 
        # # self.OR(self.maquinas.pop(), self.maquinas.pop() )
        # self.asterisco(self.maquinas.pop())
        # self.validacion(self.maquinas, self.expresion_regular)
        # self.graficar()
        #self.simulacion_afn()
        #self.parsing()
        # self.graficar()
        #afd_final = self.subset(self.maquinas[0])
        #self.graph2(afd_final)
        ####self.simulacion_afn(self.maquinas[0], 'bbaa')
        #self.graficar()
        return self.parsing()
        

        

    def concatenacion(self, maquina1, maquina2):
        # print(maquina1)
        # print(maquina2)
        # --
        #maquina2.estados[-1].tipo = 2
        estados = []
        estados = maquina2.estados[:-1]
        punto_referencia = len(maquina2.estados) -1

        for estado in maquina1.estados:
            
            if estado.tipo == 1:
                estado.etiqueta = "s" + str(punto_referencia)
                estado.tipo = 2
            
            else:
                estado.etiqueta = "s" + str((int(estado.etiqueta[1:]) + punto_referencia))

            
            for transicion in estado.transiciones:
                transicion.destino = "s" + str((int(transicion.destino[1:]) + punto_referencia))

            estados.append(estado)
        
        self.maquinas.append(AFN(estados,[],[])) 



    def asterisco(self, auotomata):
        estados = []
        estado_inicial = Estado("s0",[Transicion("s1","E"),Transicion("s"+str(len(auotomata.estados)+1),"E")],1)
        # --------
        estado_final = Estado("s"+str((len(auotomata.estados)+1)),[],3)

        
        auotomata.estados[0].tipo = 2
        auotomata.estados[-1].tipo = 2
        # auotomata.estados[-1].transiciones.append(Transicion("s0","E"))
        # auotomata.estados[-1].transiciones.append(Transicion("s"+str(len(auotomata.estados)),"E"))
        # -------

        estados.append(estado_inicial)

        for s in auotomata.estados:
            s.etiqueta = "s"+ str((int(s.etiqueta[1])+ 1))

            if len(s.transiciones) == 0:
                s.transiciones = [Transicion("s"+ str(len(auotomata.estados)+1),"E"), Transicion("s1", "E")]
            else: 
                for t in s.transiciones:
                    t.destino = "s" + str((int(t.destino[1])+ 1))
            estados.append(s)

        estados.append(estado_final)
        self.maquinas.append(AFN(estados,[],[]))

    
    def plus(self,automata):
        automata2 = copy.deepcopy(automata) #evitar conflictos con referencias
        self.asterisco(automata)
        self.concatenacion(self.maquinas.pop(),automata2)


    def OR(self,automata1,automata2):
        
        estados = []
        estado_inicial = Estado("s0",[Transicion("s1","E"),Transicion("s"+str(len(automata2.estados)+1),"E")],1)
        estado_final = Estado("s"+str(len(automata1.estados)+len(automata2.estados)+1),[],3)

        automata1.estados[0].tipo = 2 
        automata1.estados[-1].tipo = 2 

        automata2.estados[0].tipo = 2
        automata2.estados[-1].tipo = 2

        estados.append(estado_inicial)
        
        
        for s in automata2.estados:
            s.etiqueta = "s"+ str((int(s.etiqueta[1])+ 1)) 
            for t in s.transiciones:
                t.destino =  "s" + str((int(t.destino[1])+ 1))
            estados.append(s)
        

        estados[-1].transiciones =[Transicion("s"+str(len(automata1.estados)+len(automata2.estados)+1),"E")]

        for i in automata1.estados:
            i.etiqueta = "s"+ str((int(i.etiqueta[1])+len(automata2.estados)+ 1)) 
            for j in i.transiciones:
                j.destino = "s"+ str((int(j.destino[1])+len(automata2.estados)+ 1)) 
            estados.append(i)

        estados[-1].transiciones =[Transicion("s"+str(len(automata1.estados)+len(automata2.estados)+1),"E")]
        estados.append(estado_final)

        self.maquinas.append(AFN(estados,[],[]))

    def interrogacion(self,automata):
        self.paso_base("E")
        self.OR(self.maquinas.pop(),automata)

    #paso base
    #ir de estado inicial a final con un caracter
    #t1 iniical, t2 normal, t3 final ok
    def paso_base(self, caracter):
        trans = Transicion("s1", caracter)
        estado1 = Estado("s0", [trans],1)
        estadof = Estado("s1", [], 3)
        self.maquinas.append(AFN([estado1,estadof],[],trans))


    def graficar(self):
        maquina = self.maquinas[0]
        # ---
        afn = graphviz.Digraph('finite_state_machine', filename='AFN.gv')
        afn.attr(rankdir='LR', size='8,5')
        afn.attr('node', shape='doublecircle')
        afn.node('s0')
        afn.node(maquina.estados[-1].etiqueta)

        # --
        for estado in maquina.estados:
            #print(estado.tipo)
            if estado.tipo == 3:
                continue
            for transi in estado.transiciones:
                afn.attr('node', shape='circle')
                afn.edge(estado.etiqueta, transi.destino, label=transi.caracter)
        
        afn.view()
    

    def move(self,states,chr):
        response = []
        for s in states:
            for i in s.transiciones:
                #Caracter
                if i.caracter == chr:
                    estado = None
                    for st in self.maquinas[0].estados:
                        if st.etiqueta == i.destino:
                            estado = st
                    if estado is not None and estado not in response:
                        response.append(estado)
                    elif s not in response:
                        response.append(s)

        return response

    
    def eClosure(self,states):
        while True:
            siguiente =[]    
            for s in states:
                    if s.tipo == 3 and s not in siguiente:
                        siguiente.append(s)

                    for i in s.transiciones:
                        #Caracter abajo
                        if i.caracter == "E":
                            estado = None
                            for st in self.maquinas[0].estados:
                                if st.etiqueta == i.destino:
                                    estado = st
                                    break
                            if estado is not None: 
                                if estado not in siguiente:

                                    if s not in siguiente:
                                        siguiente.append(s)
                                    siguiente.append(estado)
                            elif s not in siguiente:
                                siguiente.append(s)                    
                        elif s not in siguiente:
                            siguiente.append(s)
            siguiente.sort(key =attrgetter("etiqueta"),reverse=False)
            if states == siguiente:
                return siguiente  
            states = siguiente
        return siguiente

    
    def move2(self,states,chr,maquina):
        response = []
        for s in states:
            for i in s.transiciones:
                #caracter
                if i.caracter == chr:
                    estado = None
                    for st in maquina.estados:
                        if st.label == i.destino:
                            estado = st    
                    if estado is not None:
                        if estado not in response:
                            response.append(estado)
                    elif s not in response:
                            response.append(s)

        return response



    def simulacion_afn(self,afn,cadena):
        estados = [afn.estados[0]]
        estados = self.eClosure(estados)
        for i in cadena:
            estados = self.eClosure(self.move(estados,i))

        return  afn.estados[-1] in estados

    
    
    def graph2(self,afd1):
        sf =  []
        afd = graphviz.Digraph('finite_state_machine', filename='FDA.gv')
        afd.attr(rankdir='LR', size='8,5')
        afd.attr('node', shape='doublecircle')
        afd.node('s0')
        
        for s in afd1.estados:
            if (s.tipo ==3):
                
                for t in s.transiciones:
                    print(s.etiqueta)
                    afd.attr('node', shape='doublecircle')
                    afd.edge(s.etiqueta, t.destino, label=t.caracter)
                    sf.append(s.etiqueta)
                
                if len(s.transiciones) == 0:
                    afd.attr('node', shape='doublecircle')
                    afd.node(s.etiqueta)


        for st in afd1.estados:
            for t in st.transiciones:
                if st.tipo !=3 and st.etiqueta not in sf:
                    afd.attr('node', shape='circle')
                    afd.edge(st.etiqueta, t.destino, label=t.caracter)
        afd.view()

    def subset(self,afn):
        alpha = self.a.alfabeto(self.expresion_regular)
        #funcion que devuelve alfabeto
        alpha.sort()
        afd = []
        destados = [self.eClosure([afn.estados[0]])]
        cont, indicador = 0,0
        while indicador < len(destados):
            transi = []
            cont = indicador + 1
            for c in alpha:
                temp = self.eClosure(self.move(destados[indicador],c))
                if temp in destados:
                    arr = list(filter(lambda x: x == temp,destados)) #buscar cual existe
                    pos = destados.index(arr[0])
                    transi.append(Transicion("s"+str(pos),c)) ##Apendeo transicion hacia estado repetido
                else:
                    if len(temp)== 0:
                        cont =cont -1 #validacion label, no genera ni hay repetidos
                        continue
                    if indicador > 0:
                        transi.append(Transicion("s"+str(len(destados)),c))
                    else:
                        transi.append(Transicion("s"+str(cont),c))
                    destados.append(temp)
                    cont =cont + 1

            tipo3 = False
            sf = afn.estados[-1].etiqueta #estado final actual

            for j in destados[indicador]:
                if j.etiqueta == sf:
                    tipo3 = True
                    break
            if indicador == 0:
                afd.append(Estado("s"+str(indicador),transi,1))
            else:
                afd.append(Estado("s"+str(indicador),transi,3 if tipo3 else 2))
            indicador =indicador +1
        
        return AFN(afd,[],alpha)


    def simul2(self,cadena,afd):
        estados = []
        estados.append(afd.estados[0])
        cont = 1
        for c in cadena:
            estados = self.move2(estados,c,afd)
            cont +=1
        return len(estados) > 0 and estados[0].tipo == 3

    def move2(self,states,chr,maquina): #Parametro en el aire :v, (maquinas AFD)
        response = []
        for s in states:
            for i in s.transiciones:
                if i.caracter == chr:
                    estado = None
                    for st in maquina.estados:
                        if st.etiqueta == i.destino:
                            estado = st    
                    if estado is not None:
                        if estado not in response:
                            response.append(estado)
                    elif s not in response:
                        response.append(s)
        return response




    
    


