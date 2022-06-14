
#UNIVERSIDAD DEL VALLE DE GUATEMALA
#SARA NOHEMI ZAVALA GUIETTERZ
#18893
#LENGUAJES
# --------------------------------------
import Directo
tks = {
    "id":'˂a°b°c°d°e°f°g°h°i°s˃˂˂a°b°c°d°e°f°g°h°i°s˃°˂0°1°2°3°4°5°6˃˃×',
   "numero":'˂0°1°2°3°4°5°6˃˂˂0°1°2°3°4°5°6˃˃×˂num˃',
   }
exceps = {
    "id":{},
   "numero":{},
   }
ign = []
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
