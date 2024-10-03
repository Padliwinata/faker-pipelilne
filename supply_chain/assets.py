import json
import os

from dagster import asset, MaterializeResult, MetadataValue, AssetExecutionContext
import pandas as pd

from .resources import TransactionResource
from .utils import convert_transaction_data


@asset
def transaction_data_json(context: AssetExecutionContext, resource: TransactionResource) -> MaterializeResult:
    data = resource.get_transactions_data()
    context.log.info("Data ingested")

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
        json_data = json.load(f)

    flatten_data = [convert_transaction_data(data) for data in json_data]
    df = pd.DataFrame(flatten_data)

    df.to_csv('data/transaction_data.csv', index=False)

    return MaterializeResult(
        metadata={
            'num_records': len(df),
            'preview': MetadataValue.md(df.head().to_markdown())
        }
    )


@asset(deps=[transaction_data_csv])
def clean_csv_data():
    df = pd.read_csv('data/transaction_data.csv')

    filtered_df = df[df['transaction_status'] == 'completed']
    filtered_df.to_csv('data/completed_transaction_data.csv', index=False)

    return MaterializeResult(
        metadata={
            'clean_data_num': len(filtered_df),
            'preview': MetadataValue.md(filtered_df.head().to_markdown())
        }
    )


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


