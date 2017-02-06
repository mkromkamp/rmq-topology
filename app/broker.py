
class Broker:
    ''' RabbitMQ broker definition '''
    def __init__(self, broker_definition):
        self.definition = broker_definition

    def exchanges(self):
        ''' Exchanges '''
        return [BrokerExchange(exchange)
                for exchange
                in self.definition['exchanges']]


    def queues(self):
        ''' Queues '''
        return [BrokerQueue(queue)
                for queue
                in self.definition['queues']]

    def bindings(self):
        ''' Bindings '''
        return [BrokerBinding(binding)
                for binding
                in self.definition['bindings']]

    def policies(self):
        ''' Policies '''
        return [BrokerPolicy(policy)
                for policy
                in self.definition['policies']]


class BrokerExchange:
    ''' Broker exchange '''
    def __init__(self, exchange_definition):
        self.name = exchange_definition['name']
        self.vhost = exchange_definition['vhost']
        self.type = exchange_definition['type']
        self.durable = exchange_definition['durable']
        self.auto_delete = exchange_definition['auto_delete']
        self.internal = exchange_definition['internal']
        self.arguments = exchange_definition['arguments']

    def label(self):
        ''' Exchange label '''
        template = '{} \n type: {}'
        return template.format(self.name, self.type)


class BrokerQueue:
    ''' Broker queue '''
    def __init__(self, queue_definition):
        self.name = queue_definition['name']
        self.vhost = queue_definition['vhost']
        self.durable = queue_definition['durable']
        self.auto_delete = queue_definition['auto_delete']
        self.argurments = queue_definition['arguments']

    def label(self):
        ''' Queue label '''
        template = '{}'
        return template.format(self.name)


class BrokerBinding:
    ''' Broker binding '''
    def __init__(self, binding_definition):
        self.source = binding_definition['source']
        self.destination = binding_definition['destination']
        self.destination_type = binding_definition['destination_type']
        self.vhost = binding_definition['vhost']
        self.routing_key = binding_definition['routing_key']
        self.arguments = binding_definition['arguments']

class BrokerPolicy:
    ''' Broker policy '''
    def __init__(self, policy_definition):
        self.vhost = policy_definition['vhost']
        self.pattern = policy_definition['pattern']
        self.apply_to = policy_definition['apply-to']
        self.priority = policy_definition['priority']
        self.definition = BrokerPolicyDefinition(policy_definition['definition'])

class BrokerPolicyDefinition:
    ''' Broker policy definition '''
    def __init__(self, policy_definition):
        self.message_ttl = policy_definition.get('message-ttl', None)
        self.ha_params = policy_definition['ha-params']
        self.ha_mode = policy_definition['ha-mode']
        self.ha_sync_mode = policy_definition['ha-sync-mode']
        self.dead_letter_routing_key = policy_definition.get('dead-letter-routing-key', None)
        self.dead_letter_exchange = policy_definition.get('dead-letter-exchange', None)
