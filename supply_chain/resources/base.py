from random import Random
from dagster import ConfigurableResource


class RandomizedConfigurableResource(ConfigurableResource):
    seed: int = 2
    num: int = 10

    @property
    def random(self) -> Random:
        return Random(self.seed)
