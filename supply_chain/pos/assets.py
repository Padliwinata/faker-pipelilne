from dagster import asset, AssetExecutionContext, Output, MetadataValue
import pandas as pd

from supply_chain.pos.resources import POSResource
from supply_chain.utils import convert_to_json_serializable, flatten_transaction_data


@asset
def raw_sales_data(context: AssetExecutionContext, pos_resource: POSResource) -> Output:
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
def transformed_sales_data(context: AssetExecutionContext, raw_sales_data: list[dict]) -> Output:
    df = flatten_transaction_data(raw_sales_data)
    return Output(
        value=df,
        metadata={
            'preview': MetadataValue.md(df.to_markdown())
        }
    )


@asset
def cleaned_sales_data(context: AssetExecutionContext, transformed_sales_data: pd.DataFrame) -> Output:
    cleaned_data = transformed_sales_data[transformed_sales_data['payment_status'] == 'Completed']
    return Output(
        value=cleaned_data,
        metadata={
            'preview': MetadataValue.md(cleaned_data.to_markdown())
        }
    )


@asset
def sales_summary(context: AssetExecutionContext, cleaned_sales_data: pd.DataFrame) -> Output:
    summary = {'unique_customers': cleaned_sales_data['customer_id'].nunique(),
               'total_transactions': cleaned_sales_data['transaction_id'].nunique(),
               'total_revenue': cleaned_sales_data['total_item_price'].sum(),
               'average_item_price': cleaned_sales_data['price_per_unit'].mean()}

    # Most popular item by quantity sold
    most_popular_item = cleaned_sales_data.groupby('item_name')['quantity'].sum().idxmax()
    summary['most_popular_item'] = most_popular_item

    # Most profitable item (highest total revenue by item)
    most_profitable_item = cleaned_sales_data.groupby('item_name')['total_item_price'].sum().idxmax()
    summary['most_profitable_item'] = most_profitable_item
    # summarized_data = flatten_transaction_data(cleaned_sales_data)
    # json_data = convert_to_json_serializable(summarized_data)
    # context.log.info(summarized_data)
    return Output(
        value=summary,
        metadata={
            'preview': MetadataValue.json(convert_to_json_serializable([summary]))
        }
    )


# @asset
# def payment_reconciliation_report(context: AssetExecutionContext, sales_summary: list[dict]) -> Output:
#     reconciliation_report = sales_summary
#     json_data = convert_to_json_serializable(reconciliation_report)
#     # context.log.info(reconciliation_report)
#     return Output(
#         value=reconciliation_report,
#         metadata={
#             'preview': MetadataValue.json(json_data)
#         }
#     )
