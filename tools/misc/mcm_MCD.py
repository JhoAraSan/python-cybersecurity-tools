def primo(n):
    """
    Returns a list of prime numbers up to the given number 'n'.

    Parameters:
    n (int): The upper limit for finding prime numbers.

    Returns:
    list: A list of prime numbers up to 'n'.
    """
    p=[]
    x=2
    while x<=n:
        p.append(x)
        x+=1
    sn=int(n**0.5)
    for i in range(2,sn+1):
        for j in range(2,n//i+1):
            if i*j in p:
                p.remove(i*j)
    return p

def factorizar(a):
    """
    Factorizes a given number into its prime factors.

    Parameters:
    a (int): The number to be factorized.

    Returns:
    list: A list of prime factors of the given number.
    """

    a = int(a)
    factor = []
    num = 0
    ip = iter(primo(a))
    while a != 1:
        xp = next(ip)
        if xp <= a:
            while a % xp == 0:
                a = a // xp
                factor.append(xp)
        else:
            break
    return factor

def unir(listas):
    resultado = {}
    # Recorrer cada lista en listas
    for numeros in listas:
        # Crear un contador para esta lista
        contador = {}
        for numero in numeros:
            contador[numero] = contador.get(numero, 0) + 1

        # Actualizar el resultado
        for numero, cantidad in contador.items():
            if numero not in resultado or cantidad > resultado[numero]:
                resultado[numero] = cantidad

    # Crear la lista final basada en el resultado
    resultado_lista = sorted([numero for numero, cantidad in resultado.items() for _ in range(cantidad)])
    return resultado_lista

def interseccion(listas):
    resultado=[]
    # Contabilizar los factores primos en todas las listas
    for elemento in set(listas[0]):
        cantidad_comun = min(lista.count(elemento) for lista in listas)
        resultado.extend([elemento] * cantidad_comun)
    return resultado

def mcdym(a):
    """
    Calculate the greatest common divisor (GCD) and least common multiple (LCM) of a list of numbers.

    Args:
        a (list): A list of integers.

    Returns:
        str: A string containing the factors of each number, the factors of the GCD, and the GCD value,
             the factors of the LCM, and the LCM value. If the input is not a list, returns an error message.
    """

    if isinstance(a, list):
        a = sorted([int(x) for x in a])
        lf, lfc, md, mm = [], [], 1, 1
        msm = ''
        for i in a:
            lf.append(factorizar(i))
            msm += f'Factores de {i} son: {factorizar(i)}\n'
        lfc = interseccion(lf)
        [md := md * n for n in lfc]
        msm += f'Los factores del MCD son: {lfc}, MCD={md}\n'
        lfu = unir(lf)
        [mm := mm * n for n in lfu]
        msm += f'Los factores del mcm son: {lfu}, mcm={mm}\n'
        print()
    else:
        msm = 'Error'
    return msm
# \033[32m
# con la linea anterior es que se cambian las letras de color! 
# el numero del color es entre [ y m osea el 32
if __name__ == '__main__':
    while True:
        try:
            entrada = int(input("\033[31mQue desea hacer?: \033[34m\n1) Numeros primos hasta n \n2) Factores de n \n3) mcm y mcd \n4) Salir \033[32m\nElija: "))
            match entrada:
                case 1: 
                    a=int(input("Escriba el numero: "))
                    print(primo(a))
                case 2:
                    a=int(input("Escriba el numero: "))
                    print(factorizar(a))
                case 3:
                    a=input("Escriba los numeros separados por \033[32m','\033[32m: ")
                    nums=a.split(',')
                    print(mcdym(nums))
                case 4:
                    print("Vemos!!!\nWii\nWii\nWii\nWii")
                    quit()
                case _:
                    print("Seleccion inválida. Inténtalo nuevamente.")
                    continue
        except ValueError:
            print("Entrada inválida. Inténtalo nuevamente.")
        except KeyboardInterrupt:
            print("\n\nComenzemos de Nuevo!\n")
            continue


