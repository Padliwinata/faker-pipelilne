from supply_chain.resources.base import RandomizedConfigurableResource
from supply_chain.utils import generate_fake_asset


class InventoryResource(RandomizedConfigurableResource):
    def get_inventory_data(self):
        data = generate_fake_asset(self.num)
        return data
