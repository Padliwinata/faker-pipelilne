from supply_chain.base.resource import RandomizedConfigurableResource
from supply_chain.utils import generate_fake_crm


class CustomerManagementResource(RandomizedConfigurableResource):
    def get_crm_data(self):
        data = generate_fake_crm(self.num)
        return data
