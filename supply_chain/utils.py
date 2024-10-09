import datetime
from faker import Faker
import json
import os
import random
from typing import List, Dict, Any
import numpy as np
import pandas as pd


fake = Faker()

PAYMENT_FILE_PATH = 'data/payment_data.json'


def read_payment_data():
    """
    Reads payment data from the JSON file.

    Returns:
        List[dict]: A list of payment transactions.
    """
    if not os.path.exists(PAYMENT_FILE_PATH):
        return []

    with open(PAYMENT_FILE_PATH, "r") as file:
        payment_data = json.load(file)

    return payment_data


def write_payment_data(payments_data):
    """
    Writes payment data to a JSON file.

    Args:
        payments_data (List[dict]): The list of payment transactions to write.
    """
    with open(PAYMENT_FILE_PATH, "w") as file:
        json_data = convert_to_json_serializable(payments_data)
        json.dump(json_data, file, indent=4)


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


def generate_fake_asset(num_items: int = 10):
    """
    Generates a list of fake inventory asset data.

    Args:
        num_items (int): The number of fake inventory items to generate.

    Returns:
        List[dict]: A list of dictionaries representing inventory items.
    """
    inventory_data = []

    for _ in range(num_items):
        item = {
            "item_id": fake.uuid4(),
            "product_name": fake.word().capitalize(),
            "stock_quantity": fake.random_int(min=0, max=100),
            "price_per_unit": round(fake.random_number(digits=2) + fake.random.random(), 2),
            "supplier": fake.company(),
            "last_stocked": fake.date_this_year(),
        }
        inventory_data.append(item)

    return inventory_data


def generate_fake_crm(num_customers: int = 10):
    """
    Generates a list of fake CRM data.

    Args:
        num_customers (int): The number of fake customer records to generate.

    Returns:
        List[dict]: A list of dictionaries representing CRM customer data.
    """
    crm_data = []

    for _ in range(num_customers):
        customer = {
            "customer_id": fake.uuid4(),
            "name": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "address": fake.address(),
            "loyalty_points": fake.random_int(min=0, max=1000),
            "total_spent": round(fake.random_number(digits=4) + fake.random.random(), 2),
            "signup_date": fake.date_this_decade(),
            "last_purchase": fake.date_this_year(),
        }
        crm_data.append(customer)

    return crm_data


def generate_fake_payments(num_payments: int = 1):
    """
    Retrieves payment data from the file. If the file contains fewer payments than requested,
    it will return only the available payments.

    Args:
        num_payments (int): The number of payments to retrieve.

    Returns:
        List[dict]: A list of payment transactions.
    """
    payments = read_payment_data()
    return payments[:num_payments]  # Return the first `num_payments` transactions


def generate_fake_pos(num_transactions: int = 10):
    """
    Generates a list of fake POS transactions, including payment data. Payment data is written to a file.

    Args:
        num_transactions (int): The number of POS transactions to generate.

    Returns:
        List[dict]: A list of dictionaries representing POS transactions.
    """
    pos_data = []
    payments_data = []

    for _ in range(num_transactions):
        # Simulate items purchased in a transaction
        num_items = random.randint(1, 5)
        items = []
        total_amount = 0
        for _ in range(num_items):
            item = {
                "item_name": fake.word().capitalize(),
                "quantity": random.randint(1, 3),
                "price_per_unit": round(fake.random_number(digits=2) + fake.random.random(), 2),
            }
            item_total = item["quantity"] * item["price_per_unit"]
            total_amount += item_total
            items.append(item)

        # Generate payment information
        payment_info = {
            "transaction_id": fake.uuid4(),
            "amount": round(total_amount, 2),
            "payment_method": fake.random_element(elements=["Credit Card", "Debit Card", "PayPal", "Apple Pay"]),
            "payment_status": fake.random_element(elements=["Completed", "Pending", "Failed"]),
            "transaction_date": fake.date_time_this_year(),
            "customer_id": fake.uuid4(),
            "confirmation_code": fake.bothify(text='???-#####'),
        }
        payments_data.append(payment_info)  # Add payment info to the list

        # Simulate the full POS transaction
        transaction = {
            "transaction_id": payment_info["transaction_id"],
            "customer_id": payment_info["customer_id"],
            "items": items,
            "total_amount": round(total_amount, 2),
            "payment_info": payment_info,
            "transaction_date": payment_info["transaction_date"],
        }

        pos_data.append(transaction)

    # Write the generated payments data to the file
    write_payment_data(payments_data)

    return pos_data


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


# def convert_to_json_serializable(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#     """Convert a list of customer data dictionaries to a JSON-serializable format."""
#
#     json_serializable_data = []
#
#     for record in data:
#         # Create a copy of the record to avoid modifying the original
#         serializable_record = record.copy()
#
#         # Convert datetime.date objects to string format
#         for key, value in record.items():
#             if isinstance(value, datetime.date):
#                 serializable_record[key] = value.isoformat()  # Convert to string (ISO format)
#
#         json_serializable_data.append(serializable_record)
#
#     return json_serializable_data


# recursive convert
def convert_to_json_serializable(data: Any) -> Any:
    """Convert a list of dictionaries, a single dictionary, or a complex structure to a JSON-serializable format."""

    def convert_value(value: Any) -> Any:
        """Recursively convert non-serializable types to serializable format."""
        if isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')  # Format as desired
        elif isinstance(value, np.int64):
            return int(value)  # Convert np.int64 to int
        elif isinstance(value, np.float64):
            return float(value)  # Convert np.float64 to float
        elif isinstance(value, dict):
            return convert_to_json_serializable(value)  # Recursively process dictionaries
        elif isinstance(value, list):
            return [convert_value(item) for item in value]  # Recursively process lists
        return value  # Return the value as is if not datetime or collection

    if isinstance(data, list):
        json_serializable_data = []
        for record in data:
            # Create a copy of the record to avoid modifying the original
            serializable_record = record.copy()

            # Convert all values in the record
            for key, value in serializable_record.items():
                serializable_record[key] = convert_value(value)

            json_serializable_data.append(serializable_record)
        return json_serializable_data
    elif isinstance(data, dict):
        # Process a single dictionary
        serializable_record = data.copy()
        for key, value in serializable_record.items():
            serializable_record[key] = convert_value(value)
        return serializable_record
    else:
        raise ValueError("Input must be a list of dictionaries or a single dictionary.")


def analyze_inventory(data: List[Dict[str, Any]]) -> Dict[str, Any]:
    # Create DataFrame
    df = pd.DataFrame(data)

    # Convert 'last_stocked' to datetime
    df['last_stocked'] = pd.to_datetime(df['last_stocked'])

    # Perform simple analysis
    summary = {
        'total_items': df.shape[0],
        'total_stock': df['stock_quantity'].sum(),
        'average_price': df['price_per_unit'].mean(),
        'most_recent_stocked': df['last_stocked'].max(),
        'least_recent_stocked': df['last_stocked'].min(),
    }

    # Prepare metadata for Dagster materialization
    metadata = {
        "schema": {
            "fields": [
                {"name": "total_items", "type": "int"},
                {"name": "total_stock", "type": "int"},
                {"name": "average_price", "type": "float"},
                {"name": "most_recent_stocked", "type": "datetime"},
                {"name": "least_recent_stocked", "type": "datetime"},
            ]
        },
        "values": {
            "total_items": summary['total_items'],
            "total_stock": summary['total_stock'],
            "average_price": summary['average_price'],
            "most_recent_stocked": summary['most_recent_stocked'].isoformat(),
            "least_recent_stocked": summary['least_recent_stocked'].isoformat(),
        }
    }

    return {
        "summary": summary,
        "metadata": metadata
    }
