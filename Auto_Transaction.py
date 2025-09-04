import uuid
import random
import time
from datetime import datetime
import sqlite3
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
import os

DB_FILE = "db.sqlite3"
MODEL_FILE = "isolation_forest_model.pkl"

STARTING_BALANCE = 50_00_000  # 50 lakhs
TECHCORP_NAME = "TechCorp Solutions"

# ---------- STEP 1: Create tables ----------
def init_db():
    """Initialize database and enable WAL mode."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        cursor = conn.cursor()

        # Transactions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            timestamp TEXT,
            amount REAL,
            sender TEXT,
            receiver TEXT,
            balance REAL
        )
        ''')

        # Accounts table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            account_name TEXT PRIMARY KEY,
            balance REAL
        )
        ''')

        # Balance history table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS balance_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT,
            timestamp TEXT,
            change_amount REAL,
            new_balance REAL
        )
        ''')

        # Insert TechCorp starting balance if not exists
        cursor.execute("SELECT balance FROM accounts WHERE account_name = ?", (TECHCORP_NAME,))
        if not cursor.fetchone():
            cursor.execute("INSERT INTO accounts (account_name, balance) VALUES (?, ?)",
                           (TECHCORP_NAME, STARTING_BALANCE))
        conn.commit()

# ---------- STEP 2: Load or train model ----------
def bootstrap_training_data(n=80):
    """Generate synthetic normal transaction data to start the model."""
    data = [[1000], [40000]]
    data += [[round(random.triangular(1000, 20000, 40000), 2)] for _ in range(n-2)]
    return np.array(data)

def load_or_train_model():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT amount FROM transactions")
        rows = cursor.fetchall()
    if len(rows) < 10:
        print("[INFO] Bootstrapping model with synthetic data...")
        historical_data = bootstrap_training_data()
    else:
        historical_data = np.array(rows)
    model = IsolationForest(contamination=0.2, random_state=42)
    model.fit(historical_data)
    joblib.dump(model, MODEL_FILE)
    return model

# ---------- STEP 3: Generate transactions ----------
company_names = [
    "SilverPeak Solutions", "NovaEdge Technologies", "BlueHaven Enterprises",
    "IronLeaf Systems", "Cloudspire Innovations", "BrightForge Labs",
    "Emberline Networks", "QuantumSprout Inc.", "Redwood Analytics",
    "AeroLink Dynamics", "PixelWave Studios", "Starcrest Ventures",
    "Boldstream Technologies", "ZenithPath Consulting", "LunarBay Software",
    "SwiftRock Logistics", "GreenAxis Energy", "Nexora Digital",
    "SummitCore Global", "OrionVista Systems"
]

def get_balance():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM accounts WHERE account_name = ?", (TECHCORP_NAME,))
        return cursor.fetchone()[0]

def update_balance(transaction_id, amount, is_credit):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()

        if is_credit:
            cursor.execute("UPDATE accounts SET balance = balance + ? WHERE account_name = ?",
                           (amount, TECHCORP_NAME))
        else:
            cursor.execute("UPDATE accounts SET balance = balance - ? WHERE account_name = ?",
                           (amount, TECHCORP_NAME))

        # Get updated balance
        cursor.execute("SELECT balance FROM accounts WHERE account_name = ?", (TECHCORP_NAME,))
        new_balance = cursor.fetchone()[0]

        # Save balance change history
        cursor.execute('''
            INSERT INTO balance_history (transaction_id, timestamp, change_amount, new_balance)
            VALUES (?, ?, ?, ?)
        ''', (transaction_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              amount if is_credit else -amount, new_balance))

        conn.commit()

def generate_transaction(anomaly_rate=0.3):
    amount = round(random.uniform(1000, 40000), 2)

    if random.choice([True, False]):  
        sender = TECHCORP_NAME
        receiver = random.choice(company_names)
        if get_balance() < amount:
            print("[SKIP] Insufficient balance for transaction.")
            return None
    else:
        sender = random.choice(company_names)
        receiver = TECHCORP_NAME

    if random.random() < anomaly_rate:
        anomaly_type = random.choice(["high_amount", "same_account"])
        if anomaly_type == "high_amount":
            amount = round(random.uniform(200000, 500000), 2)
        elif anomaly_type == "same_account":
            sender = receiver

    return {
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "amount": amount,
        "sender": sender,
        "receiver": receiver
    }

# ---------- STEP 4: Save to DB ----------
def save_transaction(transaction):
    if transaction['sender'] == transaction['receiver']:
        print(f"[SKIP] Self-transfer skipped: {transaction}")
        return

    if transaction['sender'] == TECHCORP_NAME:
        update_balance(transaction['transaction_id'], transaction['amount'], is_credit=False)
    elif transaction['receiver'] == TECHCORP_NAME:
        update_balance(transaction['transaction_id'], transaction['amount'], is_credit=True)

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (transaction_id, timestamp, amount, sender, receiver, balance)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            transaction['transaction_id'],
            transaction['timestamp'],
            transaction['amount'],
            transaction['sender'],
            transaction['receiver'],
            transaction.get('balance', 0)
        ))
        conn.commit()

# ---------- STEP 5: Main loop ----------
def main():
    init_db()
    model = load_or_train_model()
    print("\n[START] Real-time transaction generation & anomaly detection...\n")
    try:
        while True:
            transaction = generate_transaction()
            if transaction:
                save_transaction(transaction)
                prediction = model.predict([[transaction['amount']]])  # 1 = normal, -1 = anomaly
                bal = get_balance()
                if prediction[0] == -1:
                    print(f"[ALERT] Anomaly detected! {transaction} | Balance: ₹{bal:,.2f}")
                else:
                    print(f"[OK] Normal transaction: {transaction} | Balance: ₹{bal:,.2f}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n[STOP] Transaction generator stopped.")

if __name__ == "__main__":
    main()