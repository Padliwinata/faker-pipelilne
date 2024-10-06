from dagster import Definitions, load_assets_from_modules, AssetSelection, define_asset_job

# from . import assets  # type: ignore

from supply_chain.inventory.resources import InventoryResource
from supply_chain.crm.resources import CustomerManagementResource
from supply_chain.pos.resources import POSResource, PaymentGatewayResource

from supply_chain.pipeline import all_assets

all_resources = {
    'customer_resource': CustomerManagementResource(),
    'inventory_resource': InventoryResource(),
    'pos_resource': POSResource()
}

transaction_data_job = define_asset_job(name='ingest_transaction_data', selection=AssetSelection.all())

defs = Definitions(
    assets=all_assets,
    jobs=[transaction_data_job],
    resources=all_resources
)
