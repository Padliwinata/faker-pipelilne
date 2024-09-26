from faker import Faker
import random
import json


fake = Faker()


def generate_fake_transaction():
    # Generate fake IDs for related entities
    transaction_id = f"txn_{random.randint(1, 1000):03d}"
    store_id = f"store_{random.randint(1, 1000)}"
    terminal_id = f"terminal_{random.randint(1, 1000)}"

    # Generate a random customer ID
    customer_id = f"cust_{random.randint(1, 1000)}"

    # Generate a random employee ID
    employee_id = f"emp_{random.randint(1, 1000)}"

    # Generate a random item ID (for multiple items)
    item_ids = [f"item_{random.randint(1, 1000):03d}" for _ in range(random.randint(1, 5))]  # 1 to 5 items

    # Payment Information
    payment_method = random.choice(["credit_card", "debit_card", "cash", "digital_wallet"])
    transaction_amount = round(random.uniform(10.00, 500.00), 2)
    tax_amount = round(transaction_amount * 0.0825, 2)  # Example: 8.25% tax
    discounts = round(random.uniform(0, 50.00), 2)  # Random discount up to $50

    # Assemble the transaction data
    transaction_data = {
        "transaction_id": transaction_id,
        "timestamp": fake.date_time_this_year().isoformat() + "Z",
        "store_id": store_id,
        "terminal_id": terminal_id,
        "customer": {
            "customer_id": customer_id,
            "name": fake.name(),
            "contact": {
                "email": fake.email(),
                "phone": fake.phone_number()
            }
        },
        "payment": {
            "method": payment_method,
            "amount": transaction_amount,
            "tax_amount": tax_amount,
            "discounts": discounts
        },
        "items": [
            {
                "item_id": item_id,
                "name": fake.word().capitalize(),
                "quantity": random.randint(1, 5),  # Random quantity between 1 and 5
                "unit_price": round(random.uniform(5.00, 100.00), 2),  # Random price between $5 and $100
                "total_price": round(transaction_amount - discounts + tax_amount, 2),  # Total after discount and tax
                "category": fake.word().capitalize()
            } for item_id in item_ids
        ],
        "status": random.choice(["completed", "pending", "refunded", "canceled"]),
        "employee": {
            "employee_id": employee_id,
            "name": fake.name()
        },
        "loyalty_points": random.randint(0, 100),  # Random loyalty points
        "notes": fake.sentence(),
        "created_at": fake.date_time_this_year().isoformat() + "Z",
        "updated_at": fake.date_time_this_year().isoformat() + "Z",
        "created_by": "system",
        "updated_by": "system"
    }

    return transaction_data
