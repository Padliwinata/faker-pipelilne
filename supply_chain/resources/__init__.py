from .inventory import InventoryResource
from .pos import POSResource
from .crm import CustomerManagementResource


all_resources = {
    'pos_resource': POSResource(),
    'inventory_resource': InventoryResource(),
    'customer_resource': CustomerManagementResource()
}
