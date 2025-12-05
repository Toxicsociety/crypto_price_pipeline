# crypto_price_pipeline

A small data pipeline that fetches current cryptocurrency prices from a public API and stores them in a SQLite database for later analysis.

## Goal

Fetch prices for selected cryptocurrencies (e.g., Bitcoin, Ethereum) in a given fiat currency (e.g., USD) and persist the results in a SQL table with timestamps.

**High-level flow:**

API → Python (JSON) → transform → insert into SQL table

## Tech Stack

- **Language:** Python
- **Database:** SQLite (file-based, no external setup)
- **Libraries:**
  - `requests` – HTTP client for calling the API
  - `sqlite3` – built-in Python library for SQLite
  - `datetime` – built-in, for timestamps

## Data Model

Table: `crypto_prices`

```sql
CREATE TABLE IF NOT EXISTS crypto_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    currency TEXT NOT NULL,
    price REAL NOT NULL,
    fetched_at TEXT NOT NULL
);
