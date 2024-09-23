from slave import Slave
import socket

class Master:
    '''
    Master class

    The master is in charge of distributing and combining results from the slaves.
    '''
    def __init__(self, ip: str, port: int, n_slaves: int = 2) -> None:
        self.ip = ip
        self.port = port
        self.n_slaves = n_slaves
        self.slaves = []
        self.array = [i for i in range(1, 101)] 

    def start_master(self) -> None:
        '''
        Start the master

        The master will start listening for connections from the slaves.
        The slaves will be initiated by the master.
        It won't stop until he has received a message from all the slaves.
        He can have any number of slaves.
        '''

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip, self.port))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Se ha recibido una conexión de {addr}")
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(f"Datos recibidos {data!r}")
                    self.add_slave(Slave(addr[0], addr[1], self.ip, self.port, self.array))
                    if len(self.slaves) == self.n_slaves:
                        break
            self.start_slaves()
                               

    def add_slave(self, slave: Slave) -> None:
        self.slaves.append(slave)

    def start_slaves(self) -> None:
        n_jobs = len(self.array) / len(self.slaves)
        for i, slave in enumerate(self.slaves):
            slave.start(self.array[int(i*n_jobs):int((i+1)*n_jobs)] if i != len(self.slaves)-1 else self.array[int(i*n_jobs):])

if __name__ == "__main__":
    master = Master("192.168.81.161", 65432, 2)
    master.start_master()
