#UNIVERSIDAD DEL VALLE DE GUATEMALA
#SARA NOHEMI ZAVALA GUIETTERZ
#18893
#LENGUAJES

from numpy import empty
def transform_exp(regular_exp):
    while "˃ƒ" in regular_exp:
        base = []
        i = 0
        starting = []

        while i < len(regular_exp) - 1:
            if regular_exp[i] == "˂":
                starting.append(i)

            if regular_exp[i] == "˃":
                base.append(regular_exp[i])
                if regular_exp[i + 1] == "ƒ":
                    base.append("°")
                    base.append("ε")
                    base.append("˃")
                    base.insert(starting[-1], "˂")
                    i += 1
                    break
                else:
                    starting.pop()
            else:
                base.append(regular_exp[i])
            i += 1

        regular_exp = "".join(base) + regular_exp[i + 1:]

    if "ƒ" in regular_exp:
        while "ƒ" in regular_exp:
            i = regular_exp.find("ƒ")
            symbol = regular_exp[i - 1]

            regular_exp = regular_exp.replace(symbol + "ƒ", "˂" + symbol + "°ε˃")

    if regular_exp.count("˂") > regular_exp.count("˃"):
        for i in range(regular_exp.count("˂") - regular_exp.count("˃")):
            regular_exp += "˃"

    elif regular_exp.count("˂") < regular_exp.count("˃"):
        for i in range(regular_exp.count("˃") - regular_exp.count("˂")):
            regular_exp = "˂" + regular_exp

    return regular_exp

def add_concat(expresion):
    modified = ""
    operators = ["×", "°", "˂"]
    idx = 0
    while idx < len(expresion):

        if expresion[idx] == "×" and not ((expresion[idx + 1] in operators) or expresion[idx + 1] == "˃"):modified += expresion[idx] + "·"
        elif expresion[idx] == '×' and expresion[idx + 1] == '˂':modified += expresion[idx] + "·"
        elif not (expresion[idx] in operators) and expresion[idx + 1] == "˃":modified += expresion[idx]
        elif (not (expresion[idx] in operators) and not (expresion[idx + 1] in operators)) or (not (expresion[idx] in operators) and (expresion[idx + 1] == "˂")):modified += expresion[idx] + "·"
        else:
            modified += expresion[idx]
        idx += 1

        if idx + 1 >= len(expresion):
            modified += expresion[-1]
            break

    return modified


# Clase del nodo del afd directo
class direct_afd_node():
    def __init__(self, idx, id_in_tree, is_op, below_nodes, is_nulla):
        self.idx = idx
        self.id_in_tree = id_in_tree
        self.is_op = is_op
        self.below_nodes = below_nodes
        self.is_nulla = is_nulla

        self.first_position = []
        self.last_position = []

        if self.idx in "ε":
            self.is_nulla = True

        self.set_first_last_position()

    # Añade las primeras y ultimas posiciones del nodo en cuestion
    def set_first_last_position(self):
        if self.is_op:
            if self.idx == "°":
                # First
                self.first_position = self.below_nodes[0].first_position + self.below_nodes[1].first_position
                # Last
                self.last_position = self.below_nodes[0].last_position + self.below_nodes[1].last_position

            elif self.idx == "·":
                # First
                if self.below_nodes[0].is_nulla:
                    self.first_position = self.below_nodes[0].first_position + self.below_nodes[1].first_position
                else:
                    self.first_position += self.below_nodes[0].first_position
                # Last
                if self.below_nodes[1].is_nulla:
                    self.last_position = self.below_nodes[0].last_position + self.below_nodes[1].last_position
                else:
                    self.last_position += self.below_nodes[1].last_position

            elif self.idx == "×":
                # First
                self.first_position += self.below_nodes[0].first_position
                # Last
                self.last_position += self.below_nodes[0].last_position
        else:
            if self.idx not in "ε":
                # First
                self.first_position.append(self.id_in_tree)
                # Last
                self.last_position.append(self.id_in_tree)




