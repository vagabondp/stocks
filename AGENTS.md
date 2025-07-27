# 🧠 AGENTS.md

## Overview

This project analyzes stock options for a **bullish outlook** using modular agents. Each agent performs a specific task such as fetching data, calculating key metrics, or evaluating strategies. The application is written in Python and supports strategies like **cash-secured puts** and **covered calls**.

Agents are designed to be:
- Modular and reusable
- Stateless (where possible)
- Easy to extend

---

## Agents Directory Structure


---

## 📦 Agent Descriptions

### 1. `OptionDataFetcherAgent` (`option_data_fetcher.py`)
**Purpose:** Fetch option chain data for a given ticker and expiration date  
**Inputs:**
- `ticker` (e.g. `"AAPL"`)
- `expiration_date` (e.g. `"2025-08-01"`)

**Outputs:**
- Raw option data (JSON or DataFrame)

**Dependencies:**  
- `yfinance`, `pandas`

---

### 2. `OptionAnalyzerAgent` (`option_analyzer.py`)
**Purpose:** Analyze a single option contract and compute metrics  
**Inputs:**
- `ticker`
- `strike_price`
- `expiration_date`
- `option_type` (`"put"` or `"call"`)

**Outputs:**
- Premium  
- Delta  
- Break-even point  
- Downside to break-even  
- Annualized return  
- Weekly return

**Dependencies:**  
- `numpy`

---

### 3. `StrategyEvaluatorAgent` (`strategy_evaluator.py`)
**Purpose:** Evaluate the option's profitability and suitability for bullish strategies  
**Inputs:**
- Option metrics from analyzer
- Current stock price

**Outputs:**
- Suitability for cash-secured puts / wheel strategy
- Return on collateral
- Risk/reward summary

---

### 4. `ReportGeneratorAgent` (`report_generator.py`)
**Purpose:** Generate readable output in console or Excel format  
**Inputs:**
- Analysis results

**Outputs:**
- Table-style summary
- Optional Excel export

**Dependencies:**  
- `tabulate`, `openpyxl`, `xlsxwriter`

---

## ➕ How to Add a New Agent

1. Create a new Python module in `/agents`
2. Use this template in your file:

```python
"""
Agent: <Name>
Purpose: <Short description>
Inputs:
  - <Input 1>
  - <Input 2>
Outputs:
  - <Output 1>
  - <Output 2>
Dependencies: <List of packages>
"""
