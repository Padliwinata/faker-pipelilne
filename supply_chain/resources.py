from random import Random

from dagster import ConfigurableResource, MaterializeResult

from .utils import generate_fake_transaction


class TransactionResource(ConfigurableResource):
    seed: int

    @property
    def random(self) -> Random:
        return Random(self.seed)

    def get_transactions_data(self):
        number = self.random.randrange(40, 50)
        data = [generate_fake_transaction() for _ in range(number)]
        return data






