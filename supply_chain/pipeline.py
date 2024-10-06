from dagster import asset, AssetExecutionContext, MaterializeResult

from supply_chain.assets import all_assets
from supply_chain.utils import convert_to_json_serializable


@asset
def final_reporting(context: AssetExecutionContext, customer_segmentation: list[dict], payment_reconciliation_report: list[dict], inventory_report: list[dict]) -> MaterializeResult:
    return MaterializeResult(
        metadata={
            'customer_data': convert_to_json_serializable(customer_segmentation),
            'payment_data': convert_to_json_serializable(payment_reconciliation_report),
            'inventory_data': convert_to_json_serializable(inventory_report)
        }
    )


all_assets = all_assets + [final_reporting]
