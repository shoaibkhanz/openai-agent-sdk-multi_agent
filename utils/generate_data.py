import json
import random
from datetime import datetime
from faker import Faker
from typing import Literal, Any
from pathlib import Path

fake = Faker()
random.seed(42)

# Configuration
START_YEAR = 2020
END_YEAR = 2025
MONTHLY_TXN_COUNT = 50

# Categories list
CATEGORIES: list[str] = [
    "salary",
    "groceries",
    "mortgage",
    "car_payment",
    "investment",
    "credit_card",
    "utilities",
    "subscription",
    "entertainment",
    "dining",
    "transport",
    "savings",
]

# Category → type mapping
CATEGORY_TO_TYPE: dict[str, Literal["debit", "credit"]] = {
    "salary": "credit",
    "savings": "credit",  # considered incoming
    "investment": "debit",
    "groceries": "debit",
    "mortgage": "debit",
    "car_payment": "debit",
    "credit_card": "debit",
    "utilities": "debit",
    "subscription": "debit",
    "entertainment": "debit",
    "dining": "debit",
    "transport": "debit",
}

# Value ranges for each category
CATEGORY_AMOUNT_RANGES: dict[str, tuple[float, float]] = {
    "salary": (2800, 3200),
    "groceries": (20, 150),
    "mortgage": (900, 1300),
    "car_payment": (150, 300),
    "investment": (50, 500),
    "credit_card": (100, 700),
    "utilities": (50, 200),
    "subscription": (8, 50),
    "entertainment": (15, 120),
    "dining": (10, 100),
    "transport": (10, 80),
    "savings": (50, 500),
}


def generate_transaction(date: datetime, category: str) -> dict[str, Any]:
    """Generate a single transaction dictionary."""
    txn_type = CATEGORY_TO_TYPE[category]
    low, high = CATEGORY_AMOUNT_RANGES[category]
    amount = round(random.uniform(low, high), 2)

    # Debits are negative (money out)
    if txn_type == "debit":
        amount = -abs(amount)

    return {
        "date": date.strftime("%Y-%m-%d"),
        "year": date.year,
        "month": date.month,
        "type": txn_type,
        "category": category,
        "amount": amount,
        "description": f"{category.title()} payment at {fake.company()}",
    }


def generate_transactions(
    start_year: int, end_year: int, monthly_count: int
) -> list[dict[str, Any]]:
    """Generate transactions for each month between the given years."""
    transactions = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for _ in range(monthly_count):
                day = random.randint(1, 28)  # safe for all months
                date = datetime(year, month, day)
                category = random.choice(CATEGORIES)
                txn = generate_transaction(date, category)
                transactions.append(txn)
    return sorted(transactions, key=lambda x: x["date"])


def save_transactions_to_json(
    transactions: list[dict[str, Any]], filename: Path
) -> None:
    """Save transactions to a JSON file."""
    with open(filename, "w") as f:
        json.dump(transactions, f, indent=2)
    print(f"Saved {len(transactions)} transactions to '{filename}'")


def main():
    filepath = Path(__file__).parents[1] / "data" / "financial_transactions.json"
    transactions = generate_transactions(START_YEAR, END_YEAR, MONTHLY_TXN_COUNT)
    save_transactions_to_json(transactions, filepath)


if __name__ == "__main__":
    main()
