#UNIVERSIDAD DEL VALLE DE GUATEMALA
#SARA NOHEMI ZAVALA GUIETTERZ
#18893
#LENGUAJES

import convertidor
config_file = []

# Obtenccion del archivo a trabajar
archivo = input("Ingrese el archivo ATG --> ")
has_error = False
has_prod = False

# Abrir el archivo y revisar errores
try:
    with open(archivo, "r") as reader:
        for line in reader:
            if line != "\n":
                if "=" in line and len(line[line.find("=") + 1:-1].strip()) < 1:
                    has_error = True
                else:
                    config_file.append(line.strip())
            if "PRODUCTIONS" in line:
                has_prod = True
except:
    print("No se encontro el archivo")
    quit()
# En caso de errores
if has_error:
    print("Error encontrado")

# elif not has_prod:
#     print("No se encuentran producciones")


else:
    # Probar la generacion del scanner
    try:
        this_tokens = ""
        this_exceps = ""
        this_lexical = convertidor.Convertidor(config_file)
        for k, v in this_lexical.tokens.items():
            this_tokens += "\"" + k + "\":" + repr(v['expresion']) + ",\n   "
            this_exceps += "\"" + k + "\":" + str(v['except']) + ",\n   "

        scanner = """
#UNIVERSIDAD DEL VALLE DE GUATEMALA
#SARA NOHEMI ZAVALA GUIETTERZ
#18893
#LENGUAJES
# --------------------------------------
import Directo
tks = {
    """ + r"{}".format(this_tokens) + """}
exceps = {
    """ + f"{this_exceps}" + """}
ign = """ + f"{this_lexical.igns}" + """
chars = []

for k, v in tks.items():
    for j in v:
        if j not in "˂˃°ƒ×·" and j not in chars:
            chars.append(j)

cadena = "°".join(["˂˂" + t + "˃■˃" for t in tks.values()])

name_file = input("Ingrese el nombre del archivo: ")
file = open(name_file, "r", encoding= "utf-8")

text_to_scan = "".join(file.readlines())

dir_afd = Directo.direct_afd(cadena, chars, [t for t in tks.keys()])

actual_pos = 0
while actual_pos < len(text_to_scan):
    is_key = False
    res, actual_pos, acept = dir_afd.simulate_afd(text_to_scan, actual_pos, ign)
    
    if acept:
        for excep in exceps[dir_afd.tokens[acept]].keys():
            if res == excep:
                was_accepted = False
                print("->", repr(excep).strip(), "--> keyword", exceps[dir_afd.tokens[acept]][excep])
                is_key = True
                break
        if is_key:
            continue        
    
        if dir_afd.tokens[acept] not in ign:
            print("-> ", repr(res).strip(), "--> ", dir_afd.tokens[acept])
            continue
        

    else:
        if res != "":
            print("->", repr(res).strip(), "no se reconoce")
"""

        f = open("Scanner.py", "w", encoding="utf-8")
        f.write(scanner)
        f.close
        # En caso de cualquier error, el programa soporta que no se agrege el punto final de cualquier definicion
    except:
        print("No se pudo crear el scanner")