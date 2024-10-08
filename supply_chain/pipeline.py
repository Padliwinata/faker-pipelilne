from dagster import asset, AssetExecutionContext, MaterializeResult, load_assets_from_modules

import supply_chain.crm.assets as crm
import supply_chain.pos.assets as pos
import supply_chain.inventory.assets as inventory

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


crm_assets = load_assets_from_modules([crm], group_name='crm_assets')
pos_assets = load_assets_from_modules([pos], group_name='pos_assets')
inventory_assets = load_assets_from_modules([inventory], group_name='inventory_assets')

all_assets = crm_assets + pos_assets + inventory_assets + [final_reporting]
