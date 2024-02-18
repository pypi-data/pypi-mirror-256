from enum import Enum, unique


@unique
class BrokerTypes(Enum):
    REDIS = "redis"
    KAFKA = "kafka"
    RABBITMQ = "rabbitmq"

    @classmethod
    def from_string(cls, broker_type: str) -> 'BrokerTypes':
        try:
            return cls(broker_type.lower())
        except ValueError:
            valid_options = ', '.join([option.value for option in cls])
            raise ValueError(f"{broker_type} is not a valid BrokerOption. Valid options are: {valid_options}")