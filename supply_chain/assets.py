import json
import os

from dagster import asset, MaterializeResult

from resources import TransactionResource
from utils import convert_transaction_data


@asset
def transaction_data_json(resource: TransactionResource) -> MaterializeResult:
    data = resource.get_transactions_data()

    number_of_items = sum([len(x['items']) for x in data])

    os.makedirs('data', exist_ok=True)

    with open('data/transaction_data.json', 'w') as f:
        json.dump(data, f)

    return MaterializeResult(
        metadata={
            "number_of_transactions": len(data),
            "number_of_items_sold": number_of_items
        }
    )


@asset(deps=[transaction_data_json])
def transaction_data_csv() -> MaterializeResult:
    with open('data/transaction_data.json', 'r') as f:
        data = json.load(f)

    


# @asset(deps=[data_from_api])
# def data_from_json() -> MaterializeResult:
#     with open('data/transaction_data.json') as f:
#         data = json.load(f)
#
#     single_data = data[0]
#
#     return MaterializeResult(
#         metadata=single_data
#     )


