from faker import Faker
import random


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


def convert_transaction_data(original_data):
    """
    :param original_data: the original data param is customized to generate_fake_transaction data
    :return: flattened generate_fake_transaction return value
    """
    # Flattening customer data
    customer_data = original_data.get("customer", {})
    customer_contact = customer_data.get("contact", {})

    # Flattening payment data
    payment_data = original_data.get("payment", {})

    # Counting the number of items
    items = original_data.get("items", [])
    number_of_items = len(items)

    # Creating the flattened data structure
    flattened_data = {
        "transaction_id": original_data.get("transaction_id"),
        "timestamp": original_data.get("timestamp"),
        "store_id": original_data.get("store_id"),
        "terminal_id": original_data.get("terminal_id"),
        "customer_id": customer_data.get("customer_id"),
        "customer_name": customer_data.get("name"),
        "customer_email": customer_contact.get("email"),
        "customer_phone": customer_contact.get("phone"),
        "payment_method": payment_data.get("method"),
        "payment_amount": payment_data.get("amount"),
        "payment_tax_amount": payment_data.get("tax_amount"),
        "payment_discounts": payment_data.get("discounts"),
        "number_of_items": number_of_items,
        "transaction_status": original_data.get("status"),
        "employee_id": original_data.get("employee", {}).get("employee_id"),
        "employee_name": original_data.get("employee", {}).get("name"),
        "loyalty_points": original_data.get("loyalty_points"),
        "notes": original_data.get("notes"),
        "created_at": original_data.get("created_at"),
        "updated_at": original_data.get("updated_at"),
        "created_by": original_data.get("created_by"),
        "updated_by": original_data.get("updated_by")
    }

    return flattened_data

