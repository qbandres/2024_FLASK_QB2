

def decorador(funcion):
    def envoltura():
        print("Inicio del mensaje")
        funcion()  # Llama a la función original
        print("Fin del mensaje")
    return envoltura

# Usa el decorador para modificar el comportamiento de `imprimir_mensaje`

def imprimir_mensaje():
    print("Mensaje básico")
    
@decorador
def imprimir_saludi():
    print("hello")



# Llamada a la función decorada
imprimir_mensaje()
imprimir_saludi()