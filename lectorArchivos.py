import convertidor
#Primero vamos a definar las variables fijas quen un archivo cocol tiene

COMPILER = 'COMPILER'
BEGINCOMMENT = '(.'
ENDCOMMENT = '.)'
END = 'END'

CHARACTERS = 'CHARACTERS'
KEYWORDS = 'KEYWORDS'
TOKENS = 'TOKENS'
PRODUCTIONS = 'PRODUCTIONS'
IGNORE = 'IGNORE'
COMILLAS = '"'

PLUS = '+'
MINUS = '-'
DOT = '.'
UNTIL = '..'
ANY = 'ANY'
EXCEPTKEYWORDS = 'EXCEPT KEYWORDS'


### isBeginComment
def verificar_inicio_comentario(linea):
    comentario = ''
    linea = linea.strip()
    if linea.startswith(BEGINCOMMENT):return True, linea.split(BEGINCOMMENT,1)[1]
    return None, comentario

##isEndComment
def verificar_final_comentario(linea):
    comentario = ''
    linea = linea.strip()
    if linea.endswith(ENDCOMMENT):return True, linea.split(ENDCOMMENT,1)[0]
    return None, comentario

### compilerHeader
def get_encabezado(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(COMPILER):return linea.split(COMPILER,1)[1]
    return None

### compilerEnd
def encontrar_final(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(END):return linea.split(END,1)[1]
    return None

### whiteSpaceIgnore
def definir_ignore(linea):
    linea = linea.strip('\n').strip('\t').strip()
    if linea.startswith(IGNORE):return linea.split(IGNORE,1)[1]
    return None

##processCharacter
def pre_procesamiento(conjunto_caracteres, vocabulario):

    conjunto_caracteres = conjunto_caracteres[:-1]
    conjunto_caracteres = conjunto_caracteres.replace("'", '"')

# ----------------------------------------------------------
# Ahora definimos las variables necesarias para procesar cada uno de los caracteres
# que se van a manejar dentro de un archivo
    comillas = 0
    saltos,signo= None
    grupo_0,grupo_1 = set()
    antecesor,sucedor = ''
# ----------------------------------------------------------
    for i in range(len(conjunto_caracteres)):
        if not saltos:
            if conjunto_caracteres[i] == COMILLAS:
                comillas = comillas + 1
                continue
#-----------------------------------------------------------------------------------------------------            
            if comillas % 2 == 0:
    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------
                if (conjunto_caracteres[i] == PLUS) or (conjunto_caracteres[i] == MINUS) or ((conjunto_caracteres[i] == '.') and (conjunto_caracteres[i+1] == '.')):
                    if signo:
                        if (len(grupo_0) == 0) and (len(grupo_1) == 0):
                            grupo_0 = vocabulario[antecesor]
                            grupo_1 = vocabulario[sucedor]
                            antecesor,sucedor = ''
                        elif (len(grupo_0) == 0):
                            grupo_0 = vocabulario[antecesor]
                            antecesor = ''
                        elif (len(grupo_1) == 0):
                            grupo_1 = vocabulario[sucedor]
                            sucedor = ''
                        else:
                            pass
                        if signo == PLUS:
                            grupo_0 = grupo_0.union(grupo_1)
                        elif signo == MINUS:
                            grupo_0 = grupo_0.difference(grupo_1)
                        else:
                            s1 = list(grupo_0)
                            s2 = list(grupo_1)

                            grupo_0 = set()
                            for k in range(int(s1[0]), int(s2[0])+1):
                                grupo_0.add(k)
                        grupo_1 = set()
                        signo = None
    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------
                    if (conjunto_caracteres[i] == '.') and (conjunto_caracteres[i+1] == '.'):
                        saltos = 1
                        signo = UNTIL
                    else:
                        signo = conjunto_caracteres[i]
                    continue
    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------
                if (conjunto_caracteres[i] == 'C') and (conjunto_caracteres[i+1] == 'H') and (conjunto_caracteres[i+2] == 'R') and (conjunto_caracteres[i+3] == '('):
                    saltos = 3
                    for j in range(0,len(conjunto_caracteres)-i-4):
                        saltos = saltos + 1
                        if conjunto_caracteres[i+j+4] == ')':
                            caracter = conjunto_caracteres[i+4:i+j+4]

                            if caracter:
                                if signo:
                                    grupo_1.add(int(caracter))
                                else:
                                    grupo_0.add(int(caracter))
                            break
                else:
                    if signo:
                        sucedor = sucedor + conjunto_caracteres[i]
                    else:
                        antecesor = antecesor + conjunto_caracteres[i]
    #-----------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------
            else:
                if signo:
                    grupo_1.add(ord(conjunto_caracteres[i]))
                else:
                    grupo_0.add(ord(conjunto_caracteres[i]))
        else:
            saltos = saltos - 1    
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
    if signo:
        if (len(grupo_0) == 0) and (len(grupo_1) == 0):
            grupo_0 = vocabulario[antecesor]
            grupo_1 = vocabulario[sucedor]
        elif (len(grupo_0) == 0):
            grupo_0 = vocabulario[antecesor]
        elif (len(grupo_1) == 0):
            grupo_1 = vocabulario[sucedor]
        else:
            pass

        if signo == PLUS:
            grupo_0 = grupo_0.union(grupo_1)
        elif signo == MINUS:
            grupo_0 = grupo_0.difference(grupo_1)
        else:
            s1 = list(grupo_0)
            s2 = list(grupo_1)

            grupo_0 = set()
            for k in range(int(s1[0]), int(s2[0])+1):
                grupo_0.add(k)
        grupo_1 = set()
        signo = None
#-----------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------
    if (len(grupo_0) == 0) and (len(antecesor) != 0):
        grupo_0 = vocabulario[antecesor]
    return grupo_0

##processToken
def manenjo_de_token(setTokens, vocabulario_token):
    senial = 0
    cantidad_comillas = 0
    saltos = None
    expresionRegular = ''

    ### Se revisa si se trae la bander EXCEPT KEYWORDS
    if EXCEPTKEYWORDS in setTokens:
        senial = 1
        setTokens = setTokens.replace(EXCEPTKEYWORDS, '').strip()

    #print(setTokens)
    for i in range(len(setTokens)):
        if not saltos:
            if setTokens[i] == COMILLAS:
                cantidad_comillas = cantidad_comillas + 1
                continue
            if cantidad_comillas % 2 == 0:
                if COMILLAS in setTokens[i:]:
                    indice = setTokens[i:].index('"')
                    saltos = indice - 1
                    tokenReplace = setTokens[i:indice + i]

                else:
                    saltos = len(setTokens[i:])
                    tokenReplace = setTokens[i:]
                tokenReplaceDict = tokenReplace.replace('{', '(').replace('}', ')*').replace('[', '(').replace(']', ')?')
                for key in sorted(vocabulario_token, key=len, reverse=True):
                    if key in tokenReplaceDict:
                        preRegex = ''
                        for value in vocabulario_token[key]:
                            preRegex = preRegex + str(value) + '|'
                        tokenReplaceDict = tokenReplaceDict.replace(key, '(' + preRegex[:-1] + ')')

                expresionRegular = expresionRegular + tokenReplaceDict

            else:
                expresionRegular = expresionRegular + str(ord(setTokens[i]))

        else:
            saltos = saltos - 1

    return expresionRegular, senial