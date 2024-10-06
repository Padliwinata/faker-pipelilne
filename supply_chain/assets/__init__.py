from dagster import load_assets_from_modules

import supply_chain.assets.crm as crm
import supply_chain.assets.inventory as inventory
import supply_chain.assets.pos as pos

crm_assets = load_assets_from_modules([crm], group_name='crm_assets')
inventory_assets = load_assets_from_modules([inventory], group_name='inventory_assets')
pos_assets = load_assets_from_modules([pos], group_name='pos_assets')

all_assets = crm_assets + inventory_assets + pos_assets

