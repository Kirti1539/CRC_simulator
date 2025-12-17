# CRC Simulator (Streamlit App)

This project is an interactive **Cyclic Redundancy Check (CRC) Simulator** built using **Python and Streamlit**.  
It demonstrates how CRC is generated at the sender side and how errors are detected at the receiver side using binary division (XOR operations).

The application is designed for **learning and visualization**, showing the **step-by-step CRC division process** instead of only the final result.

---

## Features

- Accepts a binary **dataword**
- Accepts a binary **generator polynomial**
- Simulates **CRC generation** at the sender side
- Generates the **CRC code** and final **codeword**
- Simulates **bit corruption at the receiver** (user-defined positions)
- Performs CRC division again at the receiver
- Detects whether the received data is **corrupt or error-free**
- Displays **detailed step-by-step logs** of XOR operations

---

## How CRC Is Implemented

### Sender Side
1. The dataword is appended with `(length of generator − 1)` zeros.
2. Binary division using XOR is performed with the generator polynomial.
3. The remainder obtained is the **CRC code**.
4. The final **codeword** is formed by appending the CRC to the dataword.

### Receiver Side
1. The codeword is received (optionally with bit corruption).
2. CRC division is performed again using the same generator polynomial.
3. If the remainder is **all zeros**, no error is detected.
4. If the remainder contains any `1`, an error is detected.

---

## Error Simulation

The receiver can simulate transmission errors by:
- Choosing how many bits to corrupt
- Providing the **exact bit positions** to flip (1-based indexing)

This helps demonstrate how CRC detects data corruption.

---

## Tech Stack

- Python 3.10+
- Streamlit

---

## How to Run the Project

### 1. Clone the repository
```bash
git clone https://github.com/Kirti1539/CRC_simulator.git
cd CRC_simulator
