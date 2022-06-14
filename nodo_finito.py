class afd_node():
    def __init__(self, char, nodos, tipo = 1):
        self.signo = char
        self.estados = None
        self.nodos = nodos
        self.transiciones = []
        self.terminado = False
        self.final = False
        self.identidicador_unico(nodos, tipo)
    
#Aqui se tienen TODOS los estados agrupados
    def identidicador_unico(self, nodos, tipo):
        lista_estados = []
        if tipo == 1:
            lista_estados = [x.signo for x in nodos]
        elif tipo == 2:
            lista_estados = [y for y in nodos]
        lista_estados.sort()
        lista_estados = [str(final) for final in lista_estados]
        self.estados = ",".join(lista_estados)