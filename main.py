from lectorArchivos import *

# Main

fileName = input("Ingrese el nombre de su archivo ")

archivo = open(fileName, 'r', encoding='utf-8')
lineas = archivo.readlines()

identCompiler = None
identEndCompiler = None
thereIsBeginCommet = None
thereIsEndCommet = None
readCharacters = None
readKeywords = None
readTokens = None
readProductions = None
readWhitespace = None

dictCharacters = {}
dictKeywords = {}
dictTokens = {}
whiteSpace = None

pilaComentario = ''
lineaAnterior = ''
contador = 0

agrupacion = set()
for i in range(9, 128):
    agrupacion.add(i)
    agrupacion.add(241)
    agrupacion.add(209)

dictCharacters[ANY] = agrupacion


for linea in lineas:
    if not identCompiler:
        identCompiler = get_encabezado(linea)
        if identCompiler:
            identCompiler = identCompiler.strip()
        continue

    if identCompiler:
        identEndCompiler = encontrar_final(linea)
        if identEndCompiler:
            identEndCompiler = identEndCompiler.strip()

        if identEndCompiler:
            if identEndCompiler[-1] != DOT:
                identEndCompiler = identEndCompiler + DOT

            if (identEndCompiler[:-1] == identCompiler):
                break
            elif (identEndCompiler[:-1] != identCompiler):
                print("Error de COMPILER")
                exit()


    if not thereIsBeginCommet:
        thereIsBeginCommet, pilaComentario = verificar_inicio_comentario(linea)
        if thereIsBeginCommet:
            comentario = ''
            thereIsEndCommet, comentario = verificar_final_comentario(linea)

            if thereIsEndCommet:
                pilaComentario = pilaComentario + '\n' + comentario
                thereIsBeginCommet = False
                thereIsEndCommet = False

            else:
                pilaComentario = pilaComentario + '\n' + linea
            continue

    if thereIsBeginCommet:
        comentario = ''
        thereIsEndCommet, comentario = verificar_final_comentario(linea)

        if thereIsEndCommet:
            pilaComentario = pilaComentario + '\n' + comentario
            thereIsBeginCommet = False
            thereIsEndCommet = False

        else:
            pilaComentario = pilaComentario + '\n' + linea
        
        continue
    

    if linea.strip() == CHARACTERS:
        readCharacters = True
        readKeywords = False
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == KEYWORDS:
        readCharacters = False
        readKeywords = True
        readTokens = False
        readProductions = False
        continue
    elif linea.strip() == TOKENS:
        readCharacters = False
        readKeywords = False
        readTokens = True
        readProductions = False
        continue
    elif linea.strip() == PRODUCTIONS:
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = True
        continue
    elif definir_ignore(linea.strip()) != None:
        whiteSpace = definir_ignore(linea.strip()).strip()

        ### Revisar si el whiteSpace corresponde a un SET
        whiteSpace = whiteSpace.strip().replace("' '", 'CHR(32)').replace(' ', '')
        whiteSpace = whiteSpace.strip('\n').strip('\t').strip()

        if whiteSpace[-1] != DOT:
            whiteSpace = whiteSpace + '.'

        whiteSpace = pre_procesamiento(whiteSpace, dictCharacters)

        ### Determinar que no se esta leyendo CHARACTERS, TOKENS, KEYWORDS, ni PRODUCTIONS
        readCharacters = False
        readKeywords = False
        readTokens = False
        readProductions = False
        continue


    if linea.strip() == '':
        continue

    linea = lineaAnterior + linea.strip('\n').strip('\t').strip()

    contador = contador + 1


    if readCharacters:

        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        ### Extraer el ident y el SET
        particionCharacter = linea.partition('=')
        identCharacter = particionCharacter[0].strip()
        setCharacter = particionCharacter[2].strip().replace("' '", 'CHR(32)').replace(' ', '')
        setCharacter = setCharacter.strip('\n').strip('\t').strip()

        if setCharacter[-1] == DOT:
            lineaAnterior = ''

            setCharacter = pre_procesamiento(setCharacter, dictCharacters)
            dictCharacters[identCharacter] = setCharacter

        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    ### Si estoy leyendo KETWORDS los proceso como corresponde
    if readKeywords:
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue

        particionKeywords = linea.partition('=')
        identKeyword = particionKeywords[0].strip().replace(' ', '')
        setKeyword = particionKeywords[2].strip().replace('"', '').replace("' '", 'CHR(32)').replace(' ', '')
        setKeyword = setKeyword.strip('\n').strip('\t').strip()

        if setKeyword[-1] == DOT:
            lineaAnterior = ''
            dictKeywords[identKeyword] = setKeyword[:-1]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    if readTokens:
        if linea.strip('\n').strip('\t').strip()[-1] != DOT:
            lineaAnterior = linea.strip('\n').strip('\t').strip()
            continue


        particionTokens = linea.partition('=')
        identTokens = particionTokens[0].strip()
        setTokens = particionTokens[2].strip('\n').strip('\t').strip()

        if setTokens[-1] == DOT:
            lineaAnterior = ''

            expresionRegular, bandera = manenjo_de_token(setTokens[:-1], dictCharacters)

            dictTokens[identTokens] = [expresionRegular, bandera]
        else:
            lineaAnterior = linea.strip('\n').strip('\t').strip()

        continue

    if readProductions:
        pass

expresion = ''
for regex in dictTokens.values():
    expresion = expresion + '(' + regex[0] + ')#|'

expresion = expresion[:-1]
bridge.automata(expresion, dictTokens, dictKeywords, whiteSpace)
