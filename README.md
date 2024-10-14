---
# CSMA_CD

A Python-based simulation of the p-persistent CSMA/CD (Carrier Sense Multiple Access with Collision Detection) protocol, demonstrating the behavior of stations sharing a communication channel. The simulation showcases how collisions are detected, exponential backoff is applied, and data frames are transmitted.

## Features
- Simulates the p-persistent CSMA/CD protocol.
- Supports multiple stations with configurable probabilities, frame sizes, and backoff mechanisms.
- Tracks collisions, exponential backoffs, and successful transmissions.
- Customizable channel parameters like bandwidth and propagation time.

## Prerequisites
- Python 3.x

## Output
- Each station's transmission count and events are logged, tracking when collisions occur, backoff periods, and successful transmissions.
  
## Customization
You can adjust parameters like:
- `bandwidth`: Channel bandwidth in bits per millisecond.
- `Tp`: Maximum propagation time in milliseconds.
- `p`: Probability of transmission for each station.
---
