import socket

if __name__ == "__main__":
    # Create a socket object
    ip = "10.0.1.42"
    port = 20022

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print(f"Se ha recibido una conexión de {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                elif type(eval(data.decode())) == list:
                    res = sum(eval(data.decode()))
                conn.sendall(str(res).encode())