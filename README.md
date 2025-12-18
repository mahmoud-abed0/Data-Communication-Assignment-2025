# 🛡️ Data Transmission & Error Detection System

### A Robust Socket-Based Simulation of Network Reliability and Integrity

This project is a high-level simulation of **data communication protocols**, focusing on **Error Detection**, **Data Integrity**, and **network reliability**.  
It implements a **three-node socket-based architecture** (Sender → Corruptor → Receiver) to demonstrate how data behaves in a noisy network 
and how transmission errors are detected, analyzed, and in some cases corrected.

---

## 🏗️ System Architecture

The system follows a professional **Three-Node Network Model**, simulating physical-layer noise and unreliable communication channels:

### 🔹 Client 1 – Sender
- Accepts text input from the user
- Generates control information using a selected error detection method
- Encapsulates data into a structured packet
- Sends packets to the intermediate server

### 🔹 Server – Intermediate Corruptor
- Acts as a noisy network node
- Supports **manual error injection**
- Forwards corrupted packets to the receiver **without breaking packet format**

### 🔹 Client 2 – Receiver
- Decapsulates incoming packets
- Recalculates control information
- Compares sent and computed values
- Reports data integrity status (Correct / Corrupted)
- Performs **single-bit error detection for Hamming Code**

---

## 📦 Packet Format

All communication between nodes uses a unified packet structure:

DATA | METHOD | CONTROL_INFORMATION

### Example:
ahmed|Hamming|1745D0DAA564

This format ensures compatibility and clarity across all components.

---

## 🧪 Implemented Error Detection Methods

The project implements **five industry-standard error detection techniques**:

### ✅ Parity Bit
- Uses **Even Parity**
- Detects single-bit errors by counting `1` bits

### ✅ 2D Parity (Matrix Parity)
- Converts data into an **8-bit matrix**
- Computes parity for:
  - Rows
  - Columns
- Effective for detecting burst and multi-bit errors

### ✅ CRC (Cyclic Redundancy Check)
- Uses **CRC-32**
- Polynomial division via Python `zlib`
- Highly reliable for detecting transmission errors

### ✅ Hamming Code
- Generates redundancy bits based on:

2^r ≥ m + r + 1
- Uses **syndrome analysis**
- Capable of detecting (and theoretically correcting) **single-bit errors**

### ✅ Internet Checksum
- Implements **16-bit One’s Complement Sum**
- Mimics the checksum used in IP headers

---

## 💥 Professional Error Injection Suite (Server Side)

The server supports **manual selection** of error types to simulate real network corruption:

| Error Type | Description |
|-----------|------------|
| Bit Flip | Flips a single bit (1 ↔ 0) |
| Char Substitution | Replaces a character with a random ASCII symbol |
| Char Deletion | Removes a character (packet loss simulation) |
| Char Insertion | Inserts random data into the stream |
| Char Swapping | Swaps two adjacent characters |
| Multiple Bit Flips | Flips 2–4 random bits |
| Burst Error | Corrupts 3–8 consecutive bits |

This allows controlled experimentation and clear demonstration of detection behavior.

---

## 🚀 Execution Guide

To ensure correct socket initialization, run the programs **in this exact order**:

### 1️⃣ Start the Receiver
```bash
python receiver.py
```

2️⃣ Start the Corruptor Server
```bash
python server.py
```

3️⃣ Start the Sender
```bash
python sender.py
```

## 📸 Sample Output (Receiver Side)

==================================================

Alınan Veri (Received) : ?ahmed

Yöntem (Method)        : Hamming

Gönderilen Kontrol     : 1745D0DAA564

Hesaplanan Kontrol     : 25FD82D0ED65

Durum (Status)         : VERİ BOZUK (Single Bit Error Detected)

==================================================

## 📦 Required Libraries

This project requires the following Python libraries:

requests

yt-dlp

## 🔧 Installation

Run the following command in PowerShell or Command Prompt:
pip install requests yt-dlp
If pip does not work:
python -m pip install requests yt-dlp

## 💻 Technical Stack

Language: Python 3.9+

Networking: TCP/IP Socket Programming

Concurrency: Multi-threading (threading)

Encoding: UTF-8

Error Algorithms: Parity, 2D Parity, CRC-32, Hamming, Internet Checksum


## 👨‍💻 Authors

- MAHMOUD M H ABED  
- MOHAMUD AHMED MOHAMED 
- ABDELRAHMAN ELSAYED AHMED ELHADI  

**Department:** Computer Engineering  
**Course:** Socket Programming – Data Communication Assignment
