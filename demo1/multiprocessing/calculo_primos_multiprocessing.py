import multiprocessing
import time 

def es_primo(n):
    """ Devuelve True si el número n es primo, de lo contrario False. """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def calcular_primos_paralelo(rango, num_procesos):
    """ Calcula todos los números primos en un rango dado usando múltiples procesos. """
    with multiprocessing.Pool(processes=num_procesos) as pool:
        primos = pool.map(es_primo, rango)
        primos = [num for num, primo in zip(rango, primos) if primo]
        print(f"Primos encontrados: {len(primos)}")

# Definir el rango
rango = range(1, 10000000)
num_procesos = 8

# Ejecutar en paralelo
if __name__ == '__main__':
    start_time = time.time()
    calcular_primos_paralelo(rango, num_procesos=num_procesos)
    print(f"Tiempo total de ejecución: {time.time() - start_time} segundos")

