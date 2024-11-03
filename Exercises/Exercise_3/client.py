# client.py
import sys
from dask.distributed import Client
import dask.array as da
import time

def calculate_pi(num_points, chunk_size):
    xy = da.random.uniform(0, 1, size=(num_points, 2), chunks=(chunk_size, 2))
    return da.sum(da.sum(xy**2, axis=1) <= 1)

def main(num_samples, num_chunks):
    IP = "10.0.1.41"
    PORT = "69420"
    address = f"tcp://{IP}:{PORT}"
    client = Client(address)
    print("Conectado al Scheduler en", address)

    chunk_size =  num_samples//num_chunks

    start_time = time.time()

    # Configurar los chunks para la simulación
    num_inside = calculate_pi(num_samples, chunk_size).compute()
    pi_estimate_dask = num_inside * 4 / num_samples

    print(f"Estimación de Pi: {pi_estimate_dask}")
    print(f"Time elapsed: {time.time()-start_time}")
    print(f"Dask dashboard link: {client.dashboard_link}")
    client.close()

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python client.py <num_samples> <num_chunk>")
    else:
        num_samples = int(sys.argv[1])
        num_chunks = int(sys.argv[2])
        main(num_samples, num_chunks)
