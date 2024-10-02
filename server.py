import socket
import time
import math
import random


# Function to generate data
def generate_data(t):
    # Regular pattern: linear increase
    linear_component = 0.01 * t

    # Seasonal component: sine wave to simulate seasonality
    seasonal_component = 5 * math.sin(t / 100) + 5

    # Random noise: small random fluctuation
    noise = random.uniform(-0.5, 0.5)

    anomaly_chance = random.random()  # Random chance for anomalies

    # Introduce some anomalies
    if anomaly_chance < 0.05:  # 5% chance to introduce an anomaly
        return (linear_component + seasonal_component + noise) * 3  # Anomaly
    else:
        return linear_component + seasonal_component + noise


def generate_data_point():
    base_value = random.uniform(-1, 1)  # Base value
    noise = random.uniform(-0.1, 0.1)   # Random noise


# Server to stream data to a client
def start_server(host='localhost', port=8081, interval=0.2):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server started, listening on {host}:{port}")
    client_socket, addr = server_socket.accept()
    print(f"Client connected: {addr}")

    t = 0  # Initialize time for the data stream

    try:
        while True:
            # Generate the next data point
            data_point = generate_data(t)
            message = f"{data_point}\n".encode()  # Convert the data to bytes
            client_socket.sendall(message)  # Send data to the client

            t += 1
            time.sleep(interval)  # Stream at intervals of 100ms or 200ms (0.1s or 0.2s)
    except KeyboardInterrupt:
        print("Server interrupted, shutting down.")
    finally:
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    start_server(interval=0.1)  # Stream every 100ms
