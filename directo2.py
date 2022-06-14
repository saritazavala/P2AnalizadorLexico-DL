from Directo import *

class AFD:
    def __init__(self, regular_exp, acepted_symbols, passed_tokens):
        self.states = []
        self.init_state = None
        self.end_state = []
        self.accept_states = []
        self.transitions = []
        self.accepted_symbols = acepted_symbols
        self.symbols = []
        self.tokens = {}
        self.states_names = {}
        self.name_id = 0
        self.names_used = 0
        self.id_in_tree = 0
        self.nodes = []
        self.node_root = None
        self.follow_positions = {}

        regular_exp_mod = transform_exp(regular_exp)
        regular_exp_mod = add_concat(regular_exp_mod)

        # Generar arbol sintactico
        self.create_sintx_tree(regular_exp_mod)

        # Encontrar el nodos de aceptaccion
        count = 0
        for node in self.nodes:
            if node.idx == "■":
                self.end_state.append(node.id_in_tree)
                self.tokens[node.id_in_tree] = passed_tokens[count]
                count += 1

        # Obtener posiciones siguientes
        self.get_all_follow_pos()
        # Generar AFD apartir de posiciones siguientes
        self.create()

    # Obtener nombre unico, igual que en el AFD de AFN
    def set_name(self):
        possible_names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        name = possible_names[self.name_id]
        self.name_id += 1

        if self.name_id == len(possible_names):
            self.names_used += 1
            self.name_id = 0

        return name + str(self.names_used)

    def precedencia_op(self, oper):
        if oper == "°":
            return 1
        elif oper == "·":
            return 2
        elif oper == "×":
            return 3
        return -1

    # Devuelve si el primer operador tiene mayor precedencia que el segundo
    def get_precedence_of_two(self, first, second):
        pre_fir = self.precedencia_op(first)
        pre_sec = self.precedencia_op(second)
        return pre_fir >= pre_sec

    def is_accepted_symbol(self, symbol):
        accept_symbols = self.accepted_symbols + ["ε", "■"]
        if symbol in accept_symbols:
            return True
        return False

    # Crea el arbol sintactico
    def create_sintx_tree(self, reg_exp):
        characters = []
        operators = []

        # Por cada simbolo de la expresion
        for letter in reg_exp:
            # Lo agrega a los caracteres esta en el alfateto
            if self.is_accepted_symbol(letter):
                characters.append(letter)

            # Lo agrega a los operadores si es un parentesis abierto
            elif letter == "˂":
                operators.append(letter)

            # Evalua y crea la estrcura necesaria con base a lo que este dentro del parentesis
            elif letter == "˃":
                last_char = operators[-1] if operators else None
                while last_char is not None and last_char[0] != "˂":
                    local_root = self.get_operations(operators, characters)
                    characters.append(local_root)
                    last_char = operators[-1] if operators else None
                operators.pop()

            # Si es un operando primero evalua la presendencia de operandos y con base a eso genera la estructura necesaria
            else:
                last_char = operators[-1] if operators else None
                while last_char is not None and last_char not in "˂˃" and self.get_precedence_of_two(last_char, letter):
                    local_root = self.get_operations(operators, characters)
                    characters.append(local_root)
                    last_char = operators[-1] if operators else None
                operators.append(letter)

        # Para el utlimo operando que es una concatenacion con # solamente genera la raiz general
        true_root = self.get_operations(operators, characters)
        characters.append(true_root)
        self.node_root = characters.pop()

    # Genera las estructuras del arbol con base a los operandos y caracteres que se le mandan
    def get_operations(self, operators, characters):
        op = operators.pop()
        right_child = characters.pop()
        left_child = "@"

        # Agrega el simbolo al alfabeto si no esta
        if (right_child not in self.symbols) and (right_child != "@") and (right_child != "■") and (
                right_child is not None):
            self.symbols.append(right_child)

        # En caso de ser or o concat extrae al otro hijo
        if op != "×" and op != "ƒ":
            left_child = characters.pop()
            if (left_child not in self.symbols) and (left_child != "@") and (left_child != "■") and (
                    left_child is not None):
                self.symbols.append(left_child)

        # Se obtiene la estructura
        if op == "°" or op == "·":
            return self.orAndOperation(left_child, right_child, op)
        elif op == "×":
            return self.kleenOperation(right_child)

    # Generacion de las estructuras de or y concat, se usa una misma funcion ya que es casi igual solo cambia la operacion y la obtencion del anulable
    def orAndOperation(self, left_child, right_child, op):
        # Caso ya esten creados los nodos de derecha e izquierda
        if (type(left_child) == direct_afd_node) and (type(right_child) == direct_afd_node):
            if op == "°":
                local_root = direct_afd_node(op, None, True, [left_child, right_child],
                                             left_child.is_nulla or right_child.is_nulla)
                self.nodes += [local_root]
                return local_root
            elif op == "·":
                local_root = direct_afd_node(op, None, True, [left_child, right_child],
                                             left_child.is_nulla and right_child.is_nulla)
                self.nodes += [local_root]
                return local_root

        # Caso no esten creados los nodos de derecha e izquierda
        elif (type(left_child) != direct_afd_node) and (type(right_child) != direct_afd_node):
            if op == "°":
                lft_name = self.id_in_tree + 1 if left_child not in "ε" else None
                rgt_name = self.id_in_tree + 2 if right_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 2
                left_node = direct_afd_node(left_child, lft_name, False, [], False)
                right_node = direct_afd_node(right_child, rgt_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_node, right_node],
                                             left_node.is_nulla or right_node.is_nulla)

                self.nodes += [left_node, right_node, local_root]
                return local_root
            elif op == "·":
                lft_name = self.id_in_tree + 1 if left_child not in "ε" else None
                rgt_name = self.id_in_tree + 2 if right_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 2
                left_node = direct_afd_node(left_child, lft_name, False, [], False)
                right_node = direct_afd_node(right_child, rgt_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_node, right_node],
                                             left_node.is_nulla and right_node.is_nulla)
                self.nodes += [left_node, right_node, local_root]
                return local_root

        # Caso solo este creado el nodo izquierdo
        elif (type(left_child) == direct_afd_node) and (type(right_child) != direct_afd_node):
            if op == "°":
                rgt_name = self.id_in_tree + 1 if right_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 1
                right_node = direct_afd_node(right_child, rgt_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_child, right_node],
                                             left_child.is_nulla or right_node.is_nulla)
                self.nodes += [right_node, local_root]
                return local_root
            elif op == "·":
                rgt_name = self.id_in_tree + 1 if right_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 1
                right_node = direct_afd_node(right_child, rgt_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_child, right_node],
                                             left_child.is_nulla and right_node.is_nulla)
                self.nodes += [right_node, local_root]
                return local_root

        # Caso solo este creado el nodo derecho
        elif (type(left_child) != direct_afd_node) and (type(right_child) == direct_afd_node):
            if op == "°":
                lft_name = self.id_in_tree + 1 if left_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 1
                left_node = direct_afd_node(left_child, lft_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_node, right_child],
                                             left_node.is_nulla or right_child.is_nulla)
                self.nodes += [left_node, local_root]
                return local_root
            elif op == "·":
                lft_name = self.id_in_tree + 1 if left_child not in "ε" else None
                self.id_in_tree = self.id_in_tree + 1
                left_node = direct_afd_node(left_child, lft_name, False, [], False)
                local_root = direct_afd_node(op, None, True, [left_node, right_child],
                                             left_node.is_nulla and right_child.is_nulla)
                self.nodes += [left_node, local_root]
                return local_root

    # Generando la estructura de la operacion de kleen
    def kleenOperation(self, child):
        # Caso el nodo hijo ya exista
        if (type(child) == direct_afd_node):
            local_root = direct_afd_node("×", None, True, [child], True)
            self.nodes += [local_root]
            return local_root
        # Caso el nodo hijo no exista
        else:
            child_id = self.id_in_tree + 1 if child not in "ε" else None
            self.id_in_tree = self.id_in_tree + 1
            child_node = direct_afd_node(child, child_id, False, [], False)
            local_root = direct_afd_node("×", None, True, [child_node], True)
            self.nodes += [child_node, local_root]
            return local_root

    # Obtencion de las siguiente posicion teniendo en cuenta las reglas de concatenacion y kleen
    def get_all_follow_pos(self):
        for node in self.nodes:
            if not node.is_op and not node.is_nulla:
                self.set_follow_pos(node.id_in_tree, [])

            if node.idx == "·":
                c1 = node.below_nodes[0]
                c2 = node.below_nodes[1]

                for last_po in c1.last_position:
                    self.set_follow_pos(last_po, c2.first_position)

            if node.idx == "×":
                for last_po in node.last_position:
                    self.set_follow_pos(last_po, node.first_position)

    # Cambia a lista una lista de listas
    def set_to_list(self, something):
        something = {a for a in something}
        return [a for a in something]

    # Agregamos la siguiente posicion a aquellas posiciones que lo requieran
    def set_follow_pos(self, id_in_tree, follow_pos):
        if id_in_tree not in self.follow_positions.keys():
            self.follow_positions[id_in_tree] = []

        self.follow_positions[id_in_tree] += follow_pos
        self.follow_positions[id_in_tree] = self.set_to_list(self.follow_positions[id_in_tree])

    # Obtenemos un nodo en especifico dado su identificador en el arbol
    def get_node_by_id(self, id_in_tree):
        for node in self.nodes:
            if node.id_in_tree == id_in_tree:
                return node

    # Obtenemos los elementos comunes entre dos conjuntos
    def inter(self, elemt1, elemt2):
        output = [i for i in elemt1 if i in elemt2]
        return output

    # Creamos el AFD apartir del arbol generado y de las siguientes posiciones
    def create(self):
        # Obtenemos la raiz del arbol y le creamos un nodo de AFD
        first_state = self.node_root.first_position
        first_state_node = afd_node(self.set_name(), first_state, 2)
        self.states.append(first_state_node)
        self.init_state = first_state_node.idx

        inter_lst = self.inter(self.end_state, [j for j in first_state_node.nodes])

        # Si el primer estado es de aceptacion se agrega al array de estados de aceptacion
        if len(inter_lst) > 0:
            self.accept_states.append((first_state_node.idx, inter_lst[0]))

        # Mientras no se hayan realizado todos los estados se genera el AFD
        marked_states = [state.is_done for state in self.states]
        while False in marked_states:
            # Obtencion del estado a generar transiciones
            for state in self.states:
                if not state.is_done:
                    not_marked_state = state
                    break
            not_marked_state.is_done = True

            # Por cada elemento del alfabeto
            for s in self.symbols:
                # Verificamos que el elemnto del alfabeto no sea un nodo
                if type(s) != direct_afd_node:
                    siguiente_pos_entry = []
                    # Obtenemos las posiciones del arbol que el estado que estamos generando tiene
                    for node in not_marked_state.nodes:
                        if self.get_node_by_id(node).idx == s:
                            siguiente_pos_entry += self.follow_positions[node]

                    siguiente_pos_entry = self.set_to_list(siguiente_pos_entry)
                    # En caso de estar vacio se salta
                    if siguiente_pos_entry is empty:
                        continue
                    # Generamos un nuevo nodo afd
                    new_afd_node = afd_node(self.set_name(), siguiente_pos_entry, 2)

                    # Si el conjunto de estados del nuevo nodo no esta en los estados que conocemos se agrega y tambien se crea una transicion
                    if new_afd_node.states not in [state.states for state in self.states] and new_afd_node.states != "":
                        inter_lst2 = self.inter(self.end_state, [j for j in new_afd_node.nodes])
                        # Se comprueba si es un estado de aceptacion
                        if len(inter_lst2) > 0:
                            self.accept_states.append((new_afd_node.idx, inter_lst2[0]))
                        self.states.append(new_afd_node)
                        self.transitions.append([not_marked_state.idx, s, new_afd_node.idx])

                    # En caso de que el conunto de estados ya este en los estados que conocemos solo se crea la transicion
                    else:
                        self.name_id -= 1
                        for state in self.states:
                            if new_afd_node.states == state.states:
                                self.transitions.append([not_marked_state.idx, s, state.idx])

            marked_states = [state.is_done for state in self.states]
        self.states_names = dict(self.accept_states)

    # Simula el afd, cambio para el funcionamiento  del segundo proyecto
    def simulate_afd(self, cadena, position_in_str, ign):
        actual_state = self.init_state
        token = ""
        has_pair = True
        checkP = i = position_in_str
        acepting_state = None
        while has_pair and i < len(cadena):
            if cadena[i] in ign:
                i += 1
                continue

            token += cadena[i]
            actual_state = self.next_state_afd(actual_state, cadena[i])

            if actual_state in [acep_state[0] for acep_state in self.accept_states]:
                checkP = i
                acepting_state = dict(self.accept_states)[actual_state]

            if actual_state == None:
                has_pair = False
                break

            i += 1

        if len(token) != 1:
            if checkP + 1 != len(cadena):
                token = token[:-1]

        return token.strip(), checkP + 1, acepting_state

    # Funcion para mover la simulacion del AFD
    def next_state_afd(self, state, char):
        next_state = None
        for trans in self.transitions:
            if trans[0] == state and trans[1] == char:
                next_state = trans[2]
        return next_state
