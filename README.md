# Efficient-Data-Stream-Anomaly-Detection

## Introduction

This project aims to develop a real-time anomaly detection system that adapts to concept drift and seasonal variations. 

By simulating a data stream with regular patterns, seasonal elements, and random noise, we can evaluate the effectiveness of different algorithms. 

I focused on the **Simple Moving Average (SMA)** and **Z-score** methods, while also exploring the Exponential Moving Average (EMA) for potential future improvements.

_My chosen final algorithm and parameters are listed below._

## Requirements

- Use Python 3.x.
- Your code should be thoroughly documented.
- A concise explanation of your chosen algorithm and its effectiveness.
- Robust error handling and data validation.
- Limit the use of external libraries.

## How to run

- Run first the server script, and then the client.
- If you're having server issues, try replacing the port 8081 with another port in both scripts.

## Approach

### Simple Moving Average (SMA)

Calculate the average of a defined number of data points (window size) and detect deviations from this average.

#### Parameters:
- Window Size: The number of data points to consider in the average.
- Threshold: The acceptable deviation from the SMA to flag an anomaly.

#### Tested Values:
- Window Size: 5 to 10
- Threshold: 1 to 1.5

#### Anomaly Detection Logic:

- Compute the SMA for the defined window.
- Compare the latest data point against the SMA and threshold to determine if an anomaly is present.

### Z-Score

Standardise data points based on their mean and standard deviation, and determine how many standard deviations a data point is from the mean. 

#### Parameters:

- Window Size: The number of data points to calculate the mean and standard deviation.
- Threshold: The Z-score value beyond which a data point is considered an anomaly.

#### Tested Values:

- Window Size: 10 to 15
- Threshold: 1.7 to 2

#### Anomaly Detection Logic:

- Calculate the mean and standard deviation for the defined window.
- Compute the Z-score for the latest data point.
- If the Z-score exceeds the defined threshold, flag the data point as an anomaly.

### Exponential Moving Average (EMA)

Gives more weight to recent data points, making it more responsive to changes in the data stream. However, the EMA implementation has not yet been parameter-tuned for optimal performance in anomaly detection.

### Evaluation of Data Stream

To accurately evaluate the performance of the selected anomaly detection algorithms, we will introduce various sources of error and noise into the simulated data stream:

- Noise as Random Fluctuation: Introduce small random fluctuations in the data stream to simulate real-world conditions where data points can vary slightly.
- Errors as Random Chance: Implement a mechanism to introduce anomalies at random intervals (e.g., 10% chance of generating an extreme value) to simulate unusual events such as market spikes or drops.

### Chosen Algorithm and Parameters

**SMA:** Window Size: 10, Threshold: 1.2
- **Accuracy:** The Simple Moving Average (SMA) algorithm is fairly accurate in detecting anomalies, as it effectively smooths out short-term fluctuations and captures underlying trends. Its performance improves with sufficient historical data, allowing it to establish a reliable average for comparison.
- **Caveat:** At the start, the SMA may not be accurate as it doesn’t have a good idea of the average.

### Future Additions

To enhance the anomaly detection system further, several improvements and expansions can be made:

- **Parameter Tuning:** Implement a systematic approach to fine-tune the parameters of the chosen algorithms

- **Exploration of Different Algorithms:** Investigate additional anomaly detection algorithms, such as:
  - **Exponential Moving Average (EMA):** Weights recent data more heavily and can provide quicker responsiveness to changes in the data stream.
  - **ML Approaches:** Consider implementing algorithms like Isolation Forests, or decision trees that can learn from data patterns and improve anomaly detection accuracy.
  - **Statistical Tests:** Use statistical tests to complement existing methods, which may help in identifying anomalies with higher confidence levels.

- **Visualization Enhancements:** Develop better visualization tools to represent the data stream, detected anomalies, and performance metrics in real time, using popular libraries.
