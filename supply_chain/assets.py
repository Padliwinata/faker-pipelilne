import json
import os

from dagster import asset, MaterializeResult, MetadataValue, AssetExecutionContext, AssetIn, Output
import pandas as pd

from .resources import POSResource, InventoryResource, CustomerManagementResource, PaymentGatewayResource
from .utils import convert_to_json_serializable


# @asset
# def transaction_data_json(context: AssetExecutionContext, resource: TransactionResource) -> Output:
#     data = resource.get_transactions_data()
#     context.log.info("Data ingested")
#
#     number_of_items = sum([len(x['items']) for x in data])
#
#     os.makedirs('data', exist_ok=True)
#
#     with open('data/transaction_data.json', 'w') as f:
#         json.dump(data, f)
#
#     # return MaterializeResult(
#     #     metadata={
#     #         "number_of_transactions": len(data),
#     #         "number_of_items_sold": number_of_items
#     #     }
#     # )
#
#     return Output(
#         value=data,
#         metadata={
#             "number_of_transactions": len(data),
#             "number_of_items_sold": number_of_items
#         }
#     )


# @asset(ins={'transaction_data': AssetIn('transaction_data_json')})
# def ingest_more_data(transaction_data: list, resource: TransactionResource) -> MaterializeResult:
#     if len(transaction_data) <= 45:
#         transaction_data.extend(resource.get_transactions_data())
#
#     number_of_items = sum([len(x['items']) for x in transaction_data])
#
#     with open('data/transaction_data.json', 'w') as f:
#         json.dump(transaction_data, f)
#
#     return MaterializeResult(
#         metadata={
#             "number_of_transactions": len(transaction_data),
#             "number_of_items_sold": number_of_items
#         }
#     )


# @asset(deps=[transaction_data_json])
# def transaction_data_csv() -> MaterializeResult:
#     with open('data/transaction_data.json', 'r') as f:
#         json_data = json.load(f)
#
#     flatten_data = [convert_transaction_data(data) for data in json_data]
#     df = pd.DataFrame(flatten_data)
#
#     df.to_csv('data/transaction_data.csv', index=False)
#
#     return MaterializeResult(
#         metadata={
#             'num_records': len(df),
#             'preview': MetadataValue.md(df.head().to_markdown())
#         }
#     )


# @asset(deps=[transaction_data_csv])
# def clean_csv_data():
#     df = pd.read_csv('data/transaction_data.csv')
#
#     filtered_df = df[df['transaction_status'] == 'completed']
#     filtered_df.to_csv('data/completed_transaction_data.csv', index=False)
#
#     return MaterializeResult(
#         metadata={
#             'clean_data_num': len(filtered_df),
#             'preview': MetadataValue.md(filtered_df.head().to_markdown())
#         }
#     )


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


# NODES FROM CHATGPT STARTS HERE

@asset
def cleaned_sales_data(context: AssetExecutionContext, pos_resource: POSResource) -> Output:
    data = pos_resource.get_pos_data()
    json_data = convert_to_json_serializable(data)
    # context.log.info(data)
    return Output(
        value=data,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def transformed_inventory_data(context: AssetExecutionContext, inventory_resource: InventoryResource) -> Output:
    data = inventory_resource.get_inventory_data()
    json_data = convert_to_json_serializable(data)
    # context.log.info(data)
    return Output(
        value=data,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def sales_summary(context: AssetExecutionContext, cleaned_sales_data: list[dict]) -> Output:
    summarized_data = cleaned_sales_data
    json_data = convert_to_json_serializable(summarized_data)
    # context.log.info(summarized_data)
    return Output(
        value=summarized_data,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def customer_segmentation(context: AssetExecutionContext, customer_resource: CustomerManagementResource) -> Output:
    data = customer_resource.get_crm_data()
    json_data = convert_to_json_serializable(data)
    # context.log.info(data)
    return Output(
        value=data,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def payment_reconciliation_report(context: AssetExecutionContext, sales_summary: list[dict]) -> Output:
    reconciliation_report = sales_summary
    json_data = convert_to_json_serializable(reconciliation_report)
    # context.log.info(reconciliation_report)
    return Output(
        value=reconciliation_report,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def inventory_report(context: AssetExecutionContext, transformed_inventory_data: list[dict]) -> Output:
    inventory_summary = transformed_inventory_data
    json_data = convert_to_json_serializable(inventory_summary)
    # context.log.info(inventory_summary)
    return Output(
        value=inventory_summary,
        metadata={
            'preview': MetadataValue.json(json_data)
        }
    )


@asset
def final_reporting(context: AssetExecutionContext, customer_segmentation: list[dict], payment_reconciliation_report: list[dict], inventory_report: list[dict]) -> Output:
    return MaterializeResult(
        metadata={
            'customer_data': convert_to_json_serializable(customer_segmentation),
            'payment_data': convert_to_json_serializable(payment_reconciliation_report),
            'inventory_data': convert_to_json_serializable(inventory_report)
        }
    )

