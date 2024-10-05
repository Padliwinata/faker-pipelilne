from random import Random

from dagster import ConfigurableResource, MaterializeResult

from .utils import generate_fake_transaction, generate_fake_asset, generate_fake_crm, generate_fake_pos


class RandomizedConfigurableResource(ConfigurableResource):
    seed: int = 2
    num: int = 10
    @property
    def random(self) -> Random:
        return Random(self.seed)


class POSResource(RandomizedConfigurableResource):
    def get_pos_data(self):
        data = generate_fake_pos(self.num)
        return data


class InventoryResource(RandomizedConfigurableResource):
    def get_inventory_data(self):
        data = generate_fake_asset(self.num)
        return data


class CustomerManagementResource(RandomizedConfigurableResource):
    def get_crm_data(self):
        data = generate_fake_crm(self.num)
        return data


class PaymentGatewayResource(RandomizedConfigurableResource):
    def get_payment_data(self):
        data = generate_fake_pos(self.num)



