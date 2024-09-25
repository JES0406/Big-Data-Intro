import socket
import select

if __name__ == "__main__":
    port = 20022
    slaves_ips = ["10.0.1.42", "10.0.1.43"]
    array = [i for i in range(1, 101)]
    array_1 = array[:50]
    array_2 = array[50:]

    slave1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    slave2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to slaves
    slave1_socket.connect((slaves_ips[0], port))
    slave2_socket.connect((slaves_ips[1], port))

    # Send the first half to slave 1 and second half to slave 2
    slave1_socket.sendall(str(array_1).encode())
    slave2_socket.sendall(str(array_2).encode())

    # Use select to handle concurrent communication
    sockets = [slave1_socket, slave2_socket]
    total_sum = 0
    while sockets:
        readable, _, _ = select.select(sockets, [], [])

        for sock in readable:
            data = sock.recv(1024)
            if data:
                # Add the sum returned by the slave to the total
                partial_sum = int(data.decode())
                total_sum += partial_sum
                print(f"Received partial sum: {partial_sum}")
                # Remove the socket when done
                sockets.remove(sock)
                sock.close()

    print(f"Total sum: {total_sum}")