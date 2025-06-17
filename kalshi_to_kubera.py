import os
import csv
from datetime import datetime
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from kalshi import KalshiHttpClient, Environment

# Load credentials from secrets.env
load_dotenv("secrets.env")

# Use DEMO environment; change to PROD if needed
env = Environment.DEMO

# Read API key ID and path to private key
KEYID = os.getenv("DEMO_KEYID")
KEYFILE = os.getenv("DEMO_KEYFILE")

# Load the private key from PEM file
with open(KEYFILE, "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Initialize the Kalshi HTTP client
client = KalshiHttpClient(
    key_id=KEYID,
    private_key=private_key,
    environment=env
)

# Fetch open positions
positions = client.get_positions()["positions"]

# Prepare CSV data for Kubera
rows = []
for pos in positions:
    name = f"Kalshi - {pos['ticker_symbol']}"
    value = round(pos["avg_price"] * pos["contracts"], 2)
    notes = f"{pos['contracts']} contracts @ avg ${pos['avg_price']:.2f}, P/L: ${pos['realized_pnl']:.2f}"
    rows.append([name, "Alternative", value, notes])

# Write to Kubera-compatible CSV
filename = f"kalshi_kubera_{datetime.today().strftime('%Y%m%d')}.csv"
with open(filename, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Type", "Value", "Notes"])
    writer.writerows(rows)

print(f"✅ Exported Kubera CSV: {filename}")