import socket
import threading
import time

def thread_task(sock, ip, port, points):
    global inside
    sock.connect((ip, port))
    sock.sendall(str(points).encode())
    print(f"Connected to {ip}, and sent {points} points.")
    data = sock.recv(1024)
    if data:
        inside += int(data.decode())
        sock.close()

if __name__ == "__main__":
    inside = 0
    port = 20022
    slave_n = int(input("Enter the number of slaves: "))
    slave_ips = [f"10.0.1.{i}" for i in range(42, 42 + slave_n)]
    sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(slave_n)]

    points = int(input("Enter the number of points: "))
    points_per_slave = points // slave_n

    threads = []
    time_ = time.time()
    for i in range(slave_n):
        t = threading.Thread(target=thread_task, args=(sockets[i], slave_ips[i], port, points_per_slave))
        threads.append(t)
    
    for t in threads: t.start()
    for t in threads: t.join()

    pi = 4 * inside / points
    print(f"Estimated value of pi: {pi}")
    print(f"Time elapsed with {slave_n} slaves: {time.time() - time_} seconds")

    