# worker.py
import sys
from dask.distributed import Worker

def main(scheduler_address, nworkers):
    worker = Worker(scheduler_address, n_workers=int(nworkers))
    worker.start()
    print(f"Worker iniciado con {nworkers} subprocesos en {scheduler_address}")
    worker.loop.start()  # Inicia el bucle de eventos

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python worker.py <scheduler_address> <nworkers>")
    else:
        main(sys.argv[1], sys.argv[2])
