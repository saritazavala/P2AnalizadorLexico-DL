from thompson import *
from directo import *

def conversion(cadena):
    cadena2 = ""
    operadores_concatenacion = [")", "*", "+", "?"]
    for c in range(len(cadena)):
        cadena2 += cadena[c]    
        if c < len(cadena)-1:
        
            if cadena[c] in operadores_concatenacion and verificador(cadena[c+1]):
                cadena2 += "."
            elif verificador(cadena[c]) and cadena[c+1] == "(":
                print(c)
                cadena2 += "."

            elif verificador(cadena[c]) and verificador(cadena[c+1]):
                cadena2 += "."

            elif cadena[c]== ")" and cadena[c+1]=="(":
                cadena2 += "."

            elif cadena[c] =="+" and cadena[c+1] == "(":
                cadena2 += "."
            
            elif cadena[c] =="*" and cadena[c+1] == "(":
                cadena2 += "."

            elif cadena[c] =="?" and cadena[c+1] == "(":
                cadena2 += "."

    return cadena2


def verificador(caracter):
    operadores = ['*', '+','?', '.', "|", "(", ")"]
    return caracter not in operadores

        
# c = conversion("((a|b)c)*")
# a = Thompson(c)
# b = a.compilar()  


# #print(conversion("((a|b)c)*"))
# #a.graficar()
# d = a.simulacion_afn(b,'zz')

# if d:
#     print("Si")
# else:
#     print("no")


# ---------------------
#AFD = a.simul2('bbb',       )
#a = AnalizadorLexico("((a|b)|c)*")
#print(a.convertir_postfix())

# -----------------------

ex = input("Ingrese la expresion deseada --> ")
afn = None
afd = None
alpha = "abcdefghijklmnopqrstuvwxyz0123456789E"
operadores = "*|+?()"

print("  ------------------------------ ")
print("           Menu                  ")
print("  ------------------------------ ")
print("")



while True:
    print("0. Cambiar expresion regular")
    print("1. Algoritmo de Thompson")
    print("2. Algoritmo por medio de subconjuntos")
    print("3. Simulacion de AFN")
    print("4. Simulacion de AFD")
    print("5. Directo")
    print("6. Salir")
    print("")
    
    opcion = input("Elige una opcion del menu: ")
    
    c = conversion(ex)
    print(c)


    if opcion == "1":
        a = Thompson(c)
        afn = a.compilar()
        a.graficar()


    elif opcion == "2":
        if afn is not None:
            afd = a.subset(afn)
            a.graph2(afd)


    elif opcion == "0":
        ex = input("Ingrese la expresion deseada --> ")

    elif opcion == "3":
        try:
            if afn is not None:
                cadena = input("Ingrese la cadena deseada ")
                d = a.simulacion_afn(afn,cadena)
                if d:
                    print("")
                    print("Si es aceptada la cadena")
                    print("")
                else:
                    print("")
                    print("No es aceptada la cadena")
                    print("")
            else:
                print("No se ha creado ningun AFN")
        except:
            print("Cadena no valida")
    
    elif opcion == "4":
        if afd is not None:
            cadena = input("Ingrese la cadena deseada ")
            d = a.simul2(cadena, afd)
            # ----------------------------------------
            if d:
                print("")
                print("Si es aceptada la cadena")
                print("")
            else:
                print("")
                print("No es aceptada la cadena")
                print("")
        else:
            print("No se ha creado ningun AFD")
            


    elif opcion == "5":
        print("--- Directo ---")
        bandera = False
        for i in ex:
            if i not in alpha and i not in operadores:
                print("Input invalido")
                bandera = True
                break
        
        if not bandera:
            cadena = input("Ingrese la cadena que deesea evaluar: ")
            print("")

            automata_nuevo = Directo(ex)

            estados = {state.signo for state in automata_nuevo.estados}
            estado_inicial = automata_nuevo.estado0
            estados_aceoatacion_finales = {state for state in automata_nuevo.estdosAceptacion}
            trans_func = trans_func_afd(automata_nuevo.transiciones)

            verifiacacion_validez = simulate_afd(cadena, estado_inicial, estados_aceoatacion_finales, automata_nuevo.transiciones)
            print("La cadena es aceptada por el AFD --> ", verifiacacion_validez)

            print("Estados del AFN --> ", estados)
            print("Estado Inicial --> ", estado_inicial)
            print("Estados de aceptacion --> ", estados_aceoatacion_finales)
            print("Tabla de transiciones --> ", trans_func)

            local_graph(estados, estado_inicial, estados_aceoatacion_finales, trans_func, "Directo")


    elif opcion == "6":
        print("Una ayudita con la nota, gracias")
        break




