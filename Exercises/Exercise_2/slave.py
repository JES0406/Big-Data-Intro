import socket
import random
import threading

def tarea_hilo(n_points):
    global inside
    for _ in range(n_points):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            inside += 1

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 20022
    with(socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock):
        sock.bind((host, port))
        sock.listen()
        while True:
            conn, adrs = sock.accept()
            valores_pi = []
            with conn:
                print(f"Connection established from {adrs}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        points = int(data.decode())
                        inside = 0
                        thread = threading.Thread(target=tarea_hilo, args=(points,))
                        thread.start()
                        thread.join()
                        conn.sendall(str(inside).encode())
