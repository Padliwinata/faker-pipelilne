from dagster import asset, AssetExecutionContext, Output, MetadataValue

from supply_chain.crm.resources import CustomerManagementResource
from supply_chain.utils import convert_to_json_serializable


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
