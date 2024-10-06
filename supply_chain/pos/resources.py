from supply_chain.base.resource import RandomizedConfigurableResource
from supply_chain.utils import generate_fake_pos


class POSResource(RandomizedConfigurableResource):
    def get_pos_data(self):
        data = generate_fake_pos(self.num)
        return data


class PaymentGatewayResource(RandomizedConfigurableResource):
    def get_payment_data(self):
        data = generate_fake_pos(self.num)
        return data
