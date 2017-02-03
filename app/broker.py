
class Broker:
    def __init__(self, broker_definition):
        self.definition = broker_definition

    def exchange_names(self):
        return [exchange['name']
                for exchange
                in self.definition['exchanges']]
