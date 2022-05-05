import random
import copy
import pickle
import expresion_arbol
import Directo
import simulaciones_final
from Nodo import Nodo


### Funcion que nos va a permitir generar un automata AFD a partir de una expresion regular
def automata(tokensRegex, dictTokens, dictKeywords, whiteSpace):
    ### Iniciamos con las entradas de los tokens
    arbolExpresionRegularAFD, _, _ = expresion_arbol.conversionExpresionRegular(tokensRegex)
    arbolNodosExpresionRegularSustituido = Directo.sustitucionPrevia(arbolExpresionRegularAFD)
    arbolNodosExpresionRegularAFD, _, correspondencias = Directo.traduccionBase(arbolNodosExpresionRegularSustituido, 1, [])
    nodosHoja = Directo.devolverNodosHoja(arbolNodosExpresionRegularAFD, [])
    nodoRoot, nodos = Directo.definirNodosAFD(arbolNodosExpresionRegularAFD, 0, [])

    ### Unimos los nodos 
    nodosFinales = nodosHoja + nodos
    ### Se calcula la tabla de followpos 
    tablaFollowpos = Directo.followpos(nodosFinales, correspondencias)
    ### Obtener el conjunto de simbolos
    simbolos = Directo.simbolosAFDDirecta(correspondencias)
    ### Obtener las transiciones y estados (el primer estado es el estado inicial)
    dStatesAFD, dTransAFD  = Directo.traduccionAFDDirecta(nodoRoot, simbolos, tablaFollowpos, correspondencias)
    posicionesFinales = []

    ### Posicion para determinar que estados son finales
    for correspondencia in correspondencias:
        if correspondencia[0] == '#':
            posicionesFinales.append(correspondencia[1])

    ### Creamos una estructura de Nodo para simular el AFD
    afdd = Directo.convertirAFDDirectaNodo(dStatesAFD, dTransAFD, simbolos, posicionesFinales)

    ### Serializar afdd con Pickle
    with open('automata.pickle', 'wb') as f:
        pickle.dump(afdd, f)

    ### Serializar diccionario de Tokens con Pickle
    with open('tokens.pickle', 'wb') as f:
        pickle.dump(dictTokens, f)

    ### Serializar diccionario de Keywords con Pickle
    with open('keywords.pickle', 'wb') as f:
        pickle.dump(dictKeywords, f)

    ### Serializar Set de Ignore con Pickle
    with open('ignore.pickle', 'wb') as f:
        pickle.dump(whiteSpace, f)

    ### Escribir el scanner
    linea = '''
import random
import copy
import pickle
import expresion_arbol
import Directo
import simulaciones_final
from Nodo import Nodo

IGNORE = 'IGNORE'

### Automata Serializado
with open('automata.pickle', 'rb') as f:
    afdd = pickle.load(f)

### TOKENS Serializado
with open('tokens.pickle', 'rb') as f:
    tokens = pickle.load(f)

### Lectura de pickle de la definicion de TOKENS Serializado
with open('keywords.pickle', 'rb') as f:
    keywords = pickle.load(f)

### Lectura de pickle de la definicion de IGNORE Serializado
with open('ignore.pickle', 'rb') as f:
    ignoreSet = pickle.load(f)

### De aqui en adelante vamos a hacer la codificacion del Scanner
### Para la lectura de los tokens

### Primero leemos el archivo a modo de obtener una sola linea
fileName = input("Ingrese el nombre de su archivo a validar: ")
fileTxt = open(fileName, 'r', encoding='utf-8')
stringValidar = ''.join(fileTxt.readlines())
stringValidarAscii = ''
#print(tokens)

### Ahora pasamos el string a la simulacion
posicion = 0
while posicion < len(stringValidar):
    token, posicion, cadenaRetornar = simulaciones_final.simulacionAFD2(afdd, stringValidar, posicion, tokens, ignoreSet)

    ### Se limpia la cadena a retornar de los ignores
    cadenaFinal = ''
    for caracter in cadenaRetornar:
        if ignoreSet:
            caracterAscii = ord(caracter)
            if caracterAscii in ignoreSet:
                continue
        cadenaFinal = cadenaFinal + caracter

    if token:
        ### Se obtiene el valor de la bandera del token
        valorToken = tokens[token]
        valorBandera = valorToken[1]

        ### Revisar el valor de la bandera
        if (valorBandera == 1) and (cadenaFinal in keywords.values()):
            ### Imprimir que el string si es un KEYWORD
            print('KEYWORD =>', cadenaFinal)
        else:
            print(token,'=>', cadenaFinal)
    else:
        print('Error Lexico =>', cadenaFinal)'''

    archivo = open("scanner.py", "w")
    archivo.write(linea)
    archivo.close()

    print("Scanner producido")
