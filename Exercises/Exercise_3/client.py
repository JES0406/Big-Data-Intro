# client.py
import sys
import random
from dask.distributed import Client
import dask.array as da
import numpy as np

def calculate_pi(samples):
    """Estimación de Pi usando el método de Montecarlo."""
    inside_circle = 0
    for _ in range(samples):
        x, y = random.uniform(-1, 1), random.uniform(-1, 1)
        if x**2 + y**2 <= 1:
            inside_circle += 1
    return (4 * inside_circle) / samples

def main(scheduler_address, num_samples, chunk_size, workers):
    client = Client(scheduler_address)
    print("Conectado al Scheduler en", scheduler_address)

    # Configurar los chunks para la simulación
    samples = da.from_array(np.ones(num_samples, dtype=np.int32), chunks=chunk_size)

    # Mapear el cálculo de Pi sobre los chunks
    pi_estimates = samples.map_blocks(lambda chunk: calculate_pi(len(chunk)))
    pi_mean = pi_estimates.mean().compute()

    print(f"Estimación de Pi: {pi_mean}")
    client.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python client.py <scheduler_address> <num_samples> <chunk_size> <workers>")
    else:
        scheduler_address = sys.argv[1]
        num_samples = int(sys.argv[2])
        chunk_size = int(sys.argv[3])
        workers = int(sys.argv[4])
        main(scheduler_address, num_samples, chunk_size, workers)
