from dagster import asset, AssetExecutionContext, Output, MetadataValue

from supply_chain.pos.resources import POSResource
from supply_chain.utils import convert_to_json_serializable


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