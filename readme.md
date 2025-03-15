# PPP Comparison Tool

A Python application that calculates purchasing power parity (PPP) equivalents between different countries, helping users understand the real value of money across borders.

## Overview

This tool shows what an amount of money in one country would be worth in terms of purchasing power in another country, rather than just using direct currency exchange rates. It uses data from the World Bank for PPP factors and current exchange rates from an open API.

## Features

- Fetches real-time PPP data from the World Bank API
- Retrieves current exchange rates from the Exchange Rate API
- Calculates equivalent purchasing power between different countries
- Interactive CLI for country and amount selection
- Displays results with appropriate currency symbols
- Includes fallback to sample data if API calls fail

## How It Works

The application retrieves two key datasets:
1. **PPP conversion factors** from the World Bank API
2. **Currency exchange rates** from Open Exchange Rates API

It then combines these datasets to calculate the purchasing power equivalent of an amount between countries.

## Installation

1. **Clone the repository**
```
git clone https://github.com/Evilstein-debug/ppp-comparison-tool
```
2. **Create a virtual environment**
```
python -m venv venv
```
3. **Activate the virtual environment**
- Windows:
```
venv\Scripts\activate
```
- macOS/Linux:
```
source venv/bin/activate
```
4. **Install dependencies**
```
pip install -r requirements.txt
```

5. **Run the program**
```
python main.py
```