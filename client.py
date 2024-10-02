import socket
import time


# Placeholder for anomaly detection function
def is_anomaly(data_point):
    # Simple rule: any data point > 7 is considered an anomaly
    return data_point > 7


# Function to print a simple text-based graph
def print_graph(data_point, index, anomaly=False):
    graph_width = 100  # Number of characters wide for the graph
    scale = 10  # Scale to map values to characters (adjust as needed)
    position = int((data_point + scale) / (2 * scale) * graph_width)  # Normalize data point

    if position < 0:  # Keep position in range
        position = 0
    if position >= graph_width:
        position = graph_width - 1

    # Build the graph line
    graph_line = [' '] * graph_width
    graph_line[position] = '*' if not anomaly else 'X'  # Use 'X' for anomalies

    # Print the index and graph line
    print(f'{index:4d}: {"".join(graph_line)} {"(Anomaly)" if anomaly else ""}')


# Client to receive and process data
def start_client(host='localhost', port=8081):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    try:
        index = 0
        buffer = ""  # To store incomplete data between packets
        while True:
            data = client_socket.recv(1024).decode()  # Receive and decode data from the server
            if not data:
                break

            # Append new data to the buffer
            buffer += data

            # Split buffer on newlines to process complete values
            lines = buffer.split('\n')

            # Keep the last incomplete line in the buffer (if any)
            buffer = lines[-1]

            # Process each complete line (ignoring the incomplete one)
            for line in lines[:-1]:
                try:
                    data_point = float(line.strip())  # Convert to float
                    print(f"Received data: {data_point}")

                    # Detect anomalies
                    anomaly = is_anomaly(data_point)

                    # Print the data as a simple graph
                    print_graph(data_point, index, anomaly)

                    # Increment the index
                    index += 1

                    # Add a delay to simulate real-time streaming
                    time.sleep(0.2)

                except ValueError:
                    print(f"Error converting line to float: {line}")

    except KeyboardInterrupt:
        print("Client interrupted, shutting down.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    start_client()
