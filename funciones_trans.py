

import graphviz

def add_concat(expresion):
    modified = ""
    operators = ["*","|","("]
    alphabeto = "abcdefghijklmnopqrstuvwxyz0123456789E"
    idx = 0
    while idx < len(expresion):
        if expresion[idx] == "*" and ((expresion[idx+1] in alphabeto) or expresion[idx+1] == "("):
            modified += expresion[idx]+"-"
        elif not (expresion[idx] in operators) and expresion[idx+1] == ")":
            modified += expresion[idx]
        elif (not (expresion[idx] in operators) and not (expresion[idx+1] in operators)) or (not (expresion[idx] in operators) and (expresion[idx+1] == "(")):
            modified += expresion[idx]+"-"
        else:
            modified += expresion[idx]
        idx += 1

        if idx+1 >= len(expresion):
            modified += expresion[-1]
            break
    return modified



def precedencia_op(oper):
    if oper == "|":
        return 1
    elif oper == "-":
        return 2
    elif oper == "*":
        return 3
    return 0
    

def transform_exp(regular_exp, op = 1):
    final_exp = []
    to_modify = []
    inside_par = 0
    i = 0
    if "+" in regular_exp:
        while "+" in regular_exp:
            idx = regular_exp.find("+")
            if regular_exp[idx - 1] == ")":
                while i < len(regular_exp):
                    if regular_exp[i] == "(":
                        to_modify.append(i)                        
                    if regular_exp[i] == ")" and i < len(regular_exp) - 1:
                        final_exp.append(regular_exp[i])
                        if regular_exp[i + 1] == "+":
                            inside_par = i + 1
                            final_exp.append("*")
                            final_exp.append(regular_exp[to_modify.pop() : inside_par])
                            i += 1
                        else:
                            to_modify.pop()

                    else:
                        final_exp.append(regular_exp[i])
                    i += 1

                regular_exp = "".join(final_exp)
            else:
                inside = regular_exp[idx - 1]
                regular_exp = regular_exp.replace(inside + "+", "(" + inside + "*" + inside + ")")

    final_exp = []
    to_modify = []
    inside_par = 0
    i = 0

    if "?" in regular_exp:
        while "?" in regular_exp:
            idx = regular_exp.find("?")
            if regular_exp[idx - 1] == ")":
                while i < len(regular_exp):
                    if regular_exp[i] == "(":
                        to_modify.append(i)                        

                    if regular_exp[i] == ")":
                        final_exp.append(regular_exp[i])
                        if regular_exp[i + 1] == "?":
                            final_exp.append("|")
                            final_exp.append("E")
                            final_exp.append(")")
                            final_exp.insert(to_modify[-1], "(")
                            i += 1
                        else:
                            to_modify.pop()

                    else:
                        final_exp.append(regular_exp[i])
                    i += 1

                regular_exp = "".join(final_exp)
            else:
                inside = regular_exp[idx - 1]
                regular_exp = regular_exp.replace(inside + "?", "(" + inside + "|E)")

    if op == 1:
        return regular_exp

    elif op == 2:
        return "(" + regular_exp + ")#"


# Cambia a lista una lista de listas
def set_to_list(something):
    something = {a for a in something}
    return [a for a in something]

class afd_node():
    def __init__(self, char, nodos, tipo = 1):
        self.signo = char
        self.estados = None
        self.nodos = nodos
        self.transiciones = []
        self.terminado = False
        self.final = False
        self.get_unique_idx(nodos, tipo)
    

    def get_unique_idx(self, nodos, tipo):
        lista_estados = []
        if tipo == 1:
            lista_estados = [x.signo for x in nodos]
        elif tipo == 2:
            lista_estados = [y for y in nodos]
        lista_estados.sort()
        lista_estados = [str(final) for final in lista_estados]
        self.estados = ",".join(lista_estados)

# Obtener transiciones del AFD con la finalidad de graficarlo
def trans_func_afd(transitions):
    trans_f = {}
    for transition in transitions:
        init_state, char, end_state = [*transition]
        if init_state not in trans_f.keys():
            trans_f[init_state] = {}
        trans_f[init_state][char] = end_state
    return trans_f


# Funcion para mover la simulacion del AFD
def next_state_afd(state, char, transitions):
    next_state = None
    for trans in transitions:
        if trans[0] == state and trans[1] == char:
            next_state = trans[2]
    return next_state

# Util en la generacion del AFD directo o el AFD apartir de un AFN
# Simula el afd
def simulate_afd(cadena, init_state, accept_states, transitions):
    actual_state = init_state

    for char in cadena:
        actual_state = next_state_afd(actual_state, char, transitions)
        if actual_state == None:
            return False
    
    if actual_state in accept_states:
        return True
    else:
        return False


# Dibuja el grafo apartir de una funcion de transicion
def local_graph(states, init_state, end_states, trans_f, title):
    graph = graphviz.Digraph()

    for state in states:
        if state in end_states and state in init_state:
            graph.attr('node', shape = 'doubleoctagon')
            graph.node(state)
        elif state in end_states:
            graph.attr('node', shape = 'doublecircle')
            graph.node(state)
        elif state in init_state:
            graph.attr('node', shape = 'octagon')
            graph.node(state)
        else:
            graph.attr('node', shape = 'circle')
            graph.node(str(state))

    for trans in trans_f:
        for t in trans_f[trans]:
            graph.edge(trans, trans_f[trans][t], t)

    graph.render(title, view=False)