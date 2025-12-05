import requests
import sqlite3
from datetime import datetime

# 1. CONFIG
DB_PATH = "crypto_prices.db"
API_URL = "https://api.coingecko.com/api/v3/simple/price"

# We'll fetch these coins in USD
COINS = ["bitcoin", "ethereum"]
CURRENCY = "usd"


def init_db():
    """Create the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS crypto_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            currency TEXT NOT NULL,
            price REAL NOT NULL,
            fetched_at TEXT NOT NULL
        );
        """
    )

    conn.commit()
    conn.close()


def fetch_prices():
    """
    Call the CoinGecko API and return a dict with prices.
    Example response:
    {
        "bitcoin": {"usd": 12345.67},
        "ethereum": {"usd": 2345.67}
    }
    """
    params = {
        "ids": ",".join(COINS),
        "vs_currencies": CURRENCY,
    }

    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()  # Raises an error if the request failed
    data = response.json()
    return data


def save_prices_to_db(price_data):
    """
    Take the JSON from fetch_prices() and insert rows into the database.
    price_data is like:
    { "bitcoin": {"usd": 12345.67}, "ethereum": {"usd": 2345.67} }
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    fetched_at = datetime.utcnow().isoformat()

    rows_to_insert = []

    for coin, values in price_data.items():
        # coin is "bitcoin", values is {"usd": 12345.67}
        price = values.get(CURRENCY)
        if price is None:
            # Skip if the currency wasn't returned for some reason
            continue

        # We'll store the symbol in uppercase like BTC, ETH (here it's BITCOIN, ETHEREUM)
        symbol = coin.upper()
        rows_to_insert.append((symbol, CURRENCY, float(price), fetched_at))

    cursor.executemany(
        """
        INSERT INTO crypto_prices (symbol, currency, price, fetched_at)
        VALUES (?, ?, ?, ?);
        """,
        rows_to_insert,
    )

    conn.commit()
    conn.close()


def main():
    print("Initializing database...")
    init_db()

    print("Fetching prices from API...")
    price_data = fetch_prices()
    print("API response:", price_data)

    print("Saving prices to database...")
    save_prices_to_db(price_data)
    print("Done! Data inserted into crypto_prices table.")


if __name__ == "__main__":
    main()
