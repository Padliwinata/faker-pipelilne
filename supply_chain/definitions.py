from dagster import Definitions, load_assets_from_modules, AssetSelection, define_asset_job

from . import assets  # type: ignore
# from .resources import TransactionResource
from .resources import POSResource, InventoryResource, CustomerManagementResource

all_assets = load_assets_from_modules([assets])

transaction_data_job = define_asset_job(name='ingest_transaction_data', selection=AssetSelection.all())

defs = Definitions(
    assets=all_assets,
    jobs=[transaction_data_job],
    resources={
        # 'resource': TransactionResource(seed=3)
        'pos_resource': POSResource(),
        'inventory_resource': InventoryResource(),
        'customer_resource': CustomerManagementResource()
    }
)
