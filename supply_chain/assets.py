import json
import os

from dagster import asset, MaterializeResult, MetadataValue, AssetExecutionContext, AssetIn, Output
import pandas as pd

from .resources import POSResource, InventoryResource, CustomerManagementResource, PaymentGatewayResource
from .utils import convert_to_json_serializable


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

