
class AnalizadorLexico:
    def __init__(self, expresion_regular):
        self.expresion_regular =  expresion_regular


    def alfabeto(self, string):
        operadores = ['*', '+','?', '.', "|", "(", ")"]
        caracteres = []
        for x in string:
            if x not in operadores and x not in caracteres:
                caracteres.append(x)
        
        return caracteres


    
    def convertir_postfix(self):
        operadores = {'*': 5, '+': 4, '?': 3, '.': 2, '|': 1}
        postfix = []
        pila = []

        for caracter in self.expresion_regular:
            if caracter == '(':
                pila.append(caracter)

            elif caracter == ")":
                while pila[-1] != '(':
                    postfix.append(pila[-1])
                    pila = pila[:-1]
                pila = pila[:-1]
            
            elif caracter in operadores:
                while pila and operadores.get(caracter, 0) <= operadores.get(pila[-1], 0):
                    postfix.append(pila[-1])
                    pila = pila[:-1]
                pila.append(caracter)
            
            else:
                postfix.append(caracter)

        while pila:
            postfix.append(pila[-1])
            pila = pila[:-1]
        pila.append(caracter)
        print(''.join(postfix) )

        return ''.join(postfix) 
