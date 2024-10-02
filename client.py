import socket
import time


# Calculate EMA
def calculate_ema(current_value, previous_ema, alpha):
    if previous_ema is None:  # Handle first EMA calculation
        return current_value
    return (current_value * alpha) + (previous_ema * (1 - alpha))


# Calculate SMA
def calculate_sma(data_window):
    return sum(data_window) / len(data_window) if len(data_window) > 0 else 0


# Calculate Z-Score
def calculate_z_score(data_point, mean, std_dev):
    if std_dev == 0:  # Avoid division by zero
        return 0
    return (data_point - mean) / std_dev


# Anomaly detection function that swaps between EMA, SMA, and Z-Score
def detect_anomaly(data_point, history, method='EMA', alpha=0.1, window_size=10, threshold=2):
    if method == 'EMA':
        previous_ema = history[-1] if history else None
        ema = calculate_ema(data_point, previous_ema, alpha)
        # Change threshold condition to relative
        return ema, abs(data_point - ema) > threshold * ema

    elif method == 'SMA':
        if len(history) < window_size:
            history.append(data_point)
            return None, False  # Not enough data to detect anomaly
        else:
            history.pop(0)
            history.append(data_point)
        sma = calculate_sma(history)
        # Change threshold condition to relative
        return sma, abs(data_point - sma) > threshold * sma

    elif method == 'Z-Score':
        if len(history) < window_size:
            history.append(data_point)
            return None, False  # Not enough data to detect anomaly
        else:
            history.pop(0)
            history.append(data_point)
        mean = sum(history) / len(history)
        variance = sum([(x - mean) ** 2 for x in history]) / len(history)
        std_dev = variance ** 0.5
        z_score = calculate_z_score(data_point, mean, std_dev)
        return z_score, abs(z_score) > threshold  # Common thresholds for Z-Score are 2 or 3

    else:
        raise ValueError(f"Unknown method: {method}")


# Function to print a simple text-based graph
def print_graph(data_point, index, anomaly=False):
    graph_width = 50  # Number of characters wide for the graph
    max_value = 20    # Maximum expected value (adjust as needed)
    min_value = 0     # Minimum expected value

    # Normalize data point to graph width
    if data_point < min_value:
        position = 0
    elif data_point > max_value:
        position = graph_width - 1
    else:
        # Scale data to fit in the graph
        position = int((data_point - min_value) / (max_value - min_value) * (graph_width - 1))

    # Build the graph line
    graph_line = [' '] * graph_width
    graph_line[position] = '*' if not anomaly else 'X'  # Use 'X' for anomalies

    # Print the index and graph line
    print(f'{index:4d}: {"".join(graph_line)} {"(Anomaly)" if anomaly else ""}')


# Client to receive and process data
def start_client(host='localhost', port=8081, method='EMA', window_size=11, threshold=1.2, alpha=0.1):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")

    history = []  # Stores data points for SMA and Z-score calculations
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

                    # Detect anomalies based on the selected method (EMA, SMA, or Z-score)
                    moving_average, anomaly = detect_anomaly(
                        data_point, history, method=method, alpha=alpha, window_size=window_size, threshold=threshold
                    )

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
    # Start the client and specify the desired anomaly detection method
    start_client(method='SMA')  # Replace with 'SMA' or 'Z-Score' as needed
