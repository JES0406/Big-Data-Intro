# scheduler.py
from dask.distributed import Scheduler

def main():
    scheduler = Scheduler()
    scheduler.start('tcp://0.0.0.0:8786')  # Expone el Scheduler en el puerto 8786
    print("Scheduler iniciado en tcp://0.0.0.0:8786")
    scheduler.loop.start()  # Inicia el bucle de eventos

if __name__ == "__main__":
    main()
