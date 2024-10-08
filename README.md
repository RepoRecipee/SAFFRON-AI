# Portfolio Analysis Tool

This project is designed to analyze a user's mutual fund portfolio based on their transaction history. The analysis includes calculating the **total portfolio value**, **total portfolio gain**, and the **Extended Internal Rate of Return (XIRR)**. It processes the transaction data using a **First-In-First-Out (FIFO)** approach at the folio level.

---

## Features

- **Total Portfolio Value**: The sum of the current value of the remaining units for all funds.
- **Total Portfolio Gain**: The difference between the current unit value and the acquisition cost.
- **XIRR**: The internal rate of return based on cash inflows (purchases) and outflows (sales) over time.

---

## Technologies Used

- **Python**
- **Newton** from **SciPy** for XIRR calculation.
- **JSON** for handling transaction data.

---

## How It Works

1. **Input**: The program accepts a JSON file containing the user's mutual fund transaction data.
2. **Processing**: It processes the transactions using FIFO at the folio level, calculating the number of units held after each buy/sell action.
3. **Output**: The program outputs:
   - `Net unit of each fund: The total number of remaining units for each fund. `✅
   - `Net Value as of Today for Each Fund: The net value of the remaining units as of today for each fund.`✅
   - `The total value of the entire portfolio.`✅
   - `The total portfolio gain.` ✅
   - `The XIRR of the portfolio.`✅

---

## File Structure

- **`analysis.py`**: The main Python script that processes the input transaction data and calculates the portfolio value, gain, and XIRR.
- **`transaction_detail.json`**: Sample JSON file with the user's mutual fund transaction data used for testing.

---

## How to Run the Project

### Prerequisites
- Python 3.x installed on your machine.
- Required libraries:
  - `numpy`
  - `scipy`

You can install the required libraries using the following command:

```bash
pip install json datetime scipy
```
---

## Running the Analysis
### 1. Clone the repository:

```bash
git clone https://github.com/Pratham-Bajpai1/Saffron-AI-Assignment
cd portfolio-analysis
```
### 2. Run the analysis script with the provided JSON file:
```
analysis.py
```
The script will process the transactions in transaction_detail.json and print the results, including:

- Net units of each fund.
- Net value of each fund as of today.
- Total portfolio value.
- Total portfolio gain.
- XIRR.

---

## Sample Output

Net Units and Value for Each Fund:

Scheme: Aditya Birla Sun Life ELSS Tax Saver Fund
 - Remaining Units: 100.123
 - Net Value as of Today: ₹10,000.00

Total Portfolio Value: ₹4,568,788.70

Total Portfolio Gain: ₹1,150,553.97

XIRR: 23.06%

---

## Project Deliverables
- Python script (analysis.py) that processes the user's mutual fund transactions.
- JSON file (transaction_detail.json) containing sample transaction data for testing.
- Outputs include the total portfolio value, gain, and optional XIRR.

---