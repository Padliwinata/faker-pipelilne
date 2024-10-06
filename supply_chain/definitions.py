from dagster import Definitions, load_assets_from_modules, AssetSelection, define_asset_job

# from . import assets  # type: ignore
from supply_chain.resources import all_resources

from supply_chain.pipeline import all_assets

# all_assets = load_assets_from_modules([assets])

transaction_data_job = define_asset_job(name='ingest_transaction_data', selection=AssetSelection.all())

defs = Definitions(
    assets=all_assets,
    jobs=[transaction_data_job],
    resources=all_resources
)
