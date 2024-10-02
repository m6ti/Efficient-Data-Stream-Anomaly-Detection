import socket


# Client to receive and process data
def start_client(host='localhost', port=8081):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    try:
        while True:
            data = client_socket.recv(1024)  # Receive data from the server
            if not data:
                break
            data_point = float(data.decode().strip())  # Convert bytes to float
            print(f"Received data: {data_point}")
            # Here, anomaly detection logic can be added to process the data
    except KeyboardInterrupt:
        print("Client interrupted, shutting down.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
