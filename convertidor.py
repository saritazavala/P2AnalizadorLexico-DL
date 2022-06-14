#UNIVERSIDAD DEL VALLE DE GUATEMALA
#SARA NOHEMI ZAVALA GUIETTERZ
#18893
#LENGUAJES

import re
import switch
class Convertidor():
    def __init__(self, analyzer_config):
        self.comp = None
        self.tokens, self.chars, self.keys,self.productions = {}
        self.igns = []
        self.primeras_entrads(analyzer_config)
        print("Scanner generado correctamente")

    def primeras_entrads(self, configuration):
        quantity = None
        caracteres,llaves,tokens,prod, ignores = []
        section_verification, flag= ""

        for x in configuration:
            cadena = conf.split()
            #VERIFICACION SALTO DE LINEA Y LINEA EN BLANCO
            if len(cadena) > 0:
                section = cadena[0].lower()
                #VERIFICA EL ULITMO BLOQUE
                with switch(section) as s:
                    if s.case('compiler'):
                        section_verification = "compiler"
                    elif s.case('characters'):
                        section_verification = "characters"
                    elif s.case('keywords'):
                        section_verification = "keywords"
                    elif s.case('tokens'):
                        section_verification = "tokens"
                    elif s.case('productions'):
                        section_verification = "productions"
                    if s.case('ignore'):
                        ignores.append(cadena[1])
                        section_verification = "ignore"
                    if s.case('end'):
                        break
                    elif s.default():
                        print('error')



                if section_verification == "compiler":quantity = cadena[1]
                elif section_verification == "characters":caracteres.append(x)
                elif section_verification == "keywords":llaves.append(x)
                elif section_verification == "tokens":
                    flag += x
                    if x[-1] == "." or flag == "TOKENS":
                        tokens.append(flag)
                        flag = ""
                elif section_verification == "productions":
                    flag += x
                    if x[-1] == "." or flag == "PRODUCTIONS":
                        prod.append(flag)
                        flag = ""

#Saco la primera posicion
        if len(caracteres) > 0: caracteres.pop(0)
        if len(llaves) > 0: llaves.pop(0)
        if len(tokens) > 0: tokens.pop(0)
        if len(prod) > 0: prod.pop(0)

        self.comp = quantity
        self.get_chars(caracteres)

        #   IGNORE
        for ign in ignores:
            ignore = self.chars[ign]
            ignore = ignore.replace("˂", "")
            ignore = ignore.replace("˃", "")
            self.igns += ignore.split("°")

        self.get_keyw(llaves)
        self.get_tokens(tokens)
        self.productions = prod

    # Sacar caracteres
    def get_chars(self, chars):

        num_char = list(range(9, 11)) + list(range(13, 14)) + list(range(32, 127)) #toma 1 menos
        arrays = "˂°".join(chr(i) for i in num_char) + "˃"

        for i in range(len(chars)):
            temp_array = re.findall("(CHR\([0-9]*\))", chars[i])
            this_char = chars[i]
            for item in temp_array:
                this_char = this_char.replace(item, "'" + eval(item.lower()) + "'" if eval(
                    item.lower()) == "\"" else "\"" + eval(item.lower()) + "\"")

            chars[i] = this_char

        self.chars["ANY"] = arrays

        for char in chars:
            c = char.split("=", 1)
            is_single = False
            is_double = False
            actual_pos = 0
            temp_str = ""

            to_eval = c[1]
            result = ""

            for j in range(len(to_eval)):
                this_text = ""
                if to_eval[j] == "\"" and not is_double and not is_single:
                    is_double = True
                    actual_pos = j + 1
                elif to_eval[j] == "'" and not is_double and not is_single:
                    is_single = True
                    actual_pos = j + 1
                elif (to_eval[j] == "\"" and is_double) or (to_eval[j] == "'" and is_single):
                    is_double, is_single = [False, False]
                    temp_str = to_eval[actual_pos:j]

                    for k in range(len(temp_str)):
                        if k < len(temp_str) - 1:
                            this_text += temp_str[k] + "°"
                        else:
                            this_text += temp_str[k]
                    result += "˂" + this_text + "˃"
                elif to_eval[j] == "+" and not is_single and not is_double:
                    result += " + "

                elif to_eval[j] == "-" and not is_single and not is_double:
                    result += " - "
                elif not is_single and not is_double and to_eval[j] != " ":
                    result += to_eval[j]
            self.chars[c[0].replace(" ", "")] = result[:-1]

        for key, value in self.chars.items():
            final_str = ""
            if ".." in value:
                idx = value.find("..")
                item_a = value[1:idx - 1].rstrip().lstrip()
                item_b = value[idx + 3:-1].rstrip().lstrip()

                for j in self.char_range(item_a, item_b):
                    if j != item_b:
                        final_str += j + "°"
                    else:
                        final_str += j
                self.chars[key] = "˂" + final_str + "˃"

        keys = list(self.chars.keys())
        for i in range(len(keys) - 1):
            for j in range(i + 1, len(keys)):
                if keys[i] in self.chars[keys[j]]:
                    self.chars[keys[j]] = self.chars[keys[j]].replace(keys[i], self.chars[keys[i]])

        for key, value in self.chars.items():
            final_str = self.eval_str(value)
            self.chars[key] = "˂" + final_str + "˃"

    def char_range(self, item_a, item_b):
        for c in range(ord(item_a), ord(item_b) + 1):
            yield chr(c)

    def eval_str(self, tks):
        vals = []
        opers = []
        this_step = 0

        for i in range(len(tks) - 2):
            if tks[i:i + 3] == ' - ' or tks[i:i + 3] == ' + ':
                opers.insert(0, tks[i + 1])
                vals.insert(0, tks[this_step + 1:i - 1])
                this_step = i + 3
        vals.insert(0, tks[this_step + 1:-1])

        while len(opers) != 0:
            val1 = vals.pop()
            val2 = vals.pop()
            op = opers.pop()

            vals.append(self.do_operation(val1, val2, op))
        return vals[-1]


    def do_operation(self, item_a, item_b, opera):
        if opera == "+":
            res = item_a + "°" + item_b
            res = "°".join(list(dict.fromkeys(res.split("°"))))
            return res
        if opera == "-":
            res = "°".join(list(set(item_a.split("°")) - set(item_b.split("°"))))
            return res
        return -1


    def get_keyw(self, keywords):
        for key in keywords:
            key = key.replace(" ", "")
            keyw, w = key.split("=")
            w = w[:-1]
            self.keys[w.replace("\"", "")] = keyw.replace("\"", "")


    def get_tokens(self, tokens):
        my_chars = list(self.chars.keys())
        my_chars.sort(key=len)
        my_chars.reverse()

        for tk in tokens:
            this_tk = tk.split("=", 1)
            is_double = False
            actual_pos = 0
            temp_str = ""
            name = this_tk[0].replace(" ", "")
            to_eval = this_tk[1]
            result = ""

            for i in range(len(to_eval)):
                this_text = ""
                if to_eval[i] == "\"" and not is_double:
                    is_double = True
                    actual_pos = i + 1
                elif to_eval[i] == "\"" and is_double:
                    is_double = False
                    temp_str = to_eval[actual_pos:i]
                    for j in range(len(temp_str)):
                        this_text += temp_str[j]
                    result += "˂" + this_text + "˃"
                elif not is_double and to_eval[i] != " ":
                    result += to_eval[i]

            result = result.replace("|", "°")
            self.tokens[name] = {}
            self.tokens[name]['expresion'] = result[:-1]
            self.tokens[name]['except'] = {}

        for key, value in self.tokens.items():
            if "EXCEPT" in value["expresion"]:
                exceps = value["expresion"].split("EXCEPT")
                self.tokens[key]["expresion"] = exceps[0]
                if exceps[1].replace(".", "") == "KEYWORDS":self.tokens[key]["except"] = self.keys
            if "{" in value["expresion"] and "}" in value["expresion"]:
                self.tokens[key]['expresion'] = self.tokens[key]['expresion'].replace('{', '˂')
                self.tokens[key]['expresion'] = self.tokens[key]['expresion'].replace('}', '˃×')
            if '[' in value['expresion'] and ']' in value['expresion']:
                self.tokens[key]['expresion'] = self.tokens[key]['expresion'].replace('[', '˂')
                self.tokens[key]['expresion'] = self.tokens[key]['expresion'].replace(']', '˃ƒ')

        for key, value in self.tokens.items():
            new_tk = value["expresion"]
            for chr in my_chars:
                if chr in value["expresion"]:
                    new_tk = new_tk.replace(chr, self.chars[chr])
            value["expresion"] = new_tk


##https://sites.google.com/site/structuredparsing/simplexmlparser/coco-r-lexer

