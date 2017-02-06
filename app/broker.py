

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
        return [BrokerQueue(queue, self.queue_policies(queue['name']))
                for queue
                in self.definition['queues']]

    def bindings(self):
        ''' Bindings '''
        return [BrokerBinding(binding)
                for binding
                in self.definition['bindings']]

    def queue_policies(self, queue_name):
        ''' Queue policy, if any '''
        return [policy
                for policy
                in self.policies()
                if policy.pattern == queue_name]

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
        label = '<<b>{}</b> <br />'.format(self.name)
        for key, value in self.__dict__.items():
            if value and key != 'name':
                label = '<br />'.join((label, '{}: {}'.format(key, value)))

        return '{}>'.format(label)


class BrokerQueue:
    ''' Broker queue '''
    def __init__(self, queue_definition, policies):
        self.name = queue_definition['name']
        self.vhost = queue_definition['vhost']
        self.durable = queue_definition['durable']
        self.auto_delete = queue_definition['auto_delete']
        self.argurments = queue_definition['arguments']
        self.policies = policies

    def label(self):
        ''' Queue label '''
        label = '<<b>{}</b> <br />'.format(self.name)
        for policy in self.policies:
            label = '\n'.join((label, policy.definition.label()))

        return '{}>'.format(label)


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
        self.ha_params = policy_definition.get('ha-params', None)
        self.ha_mode = policy_definition.get('ha-mode', None)
        self.ha_sync_mode = policy_definition.get('ha-sync-mode', None)
        self.dead_letter_routing_key = policy_definition.get('dead-letter-routing-key', None)
        self.dead_letter_exchange = policy_definition.get('dead-letter-exchange', None)

    def label(self):
        ''' Policy defintion label '''
        label = ''
        for key, value in self.__dict__.items():
            if value:
                label = '<br />'.join((label, '{}: {}'.format(key, value)))

        return label
