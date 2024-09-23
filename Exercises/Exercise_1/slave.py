import socket

class Slave:
    def __init__(self, ip: str, port: int, master_ip: str, master_port: int, array: list) -> None:
        self.ip = ip
        self.port = port
        self.master_ip = master_ip
        self.master_port = master_port
        self.array = array

    def start(self) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.master_ip, self.master_port))
            result = 0
            for i in self.array:
                result += i
            s.sendall(str(result).encode())
            data = s.recv(1024)
            print(f"Datos recibidos {data!r}")
            s.close()