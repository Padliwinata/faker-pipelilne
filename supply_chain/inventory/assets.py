from dagster import asset, AssetExecutionContext, Output, MetadataValue

from supply_chain.inventory.resources import InventoryResource
from supply_chain.utils import convert_to_json_serializable


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
