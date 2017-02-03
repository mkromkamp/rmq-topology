import argparse
import json

import pygraphviz as pgv
from broker import Broker

def parse_args():
    ''' Get cli args '''
    parser = argparse.ArgumentParser(description='RabbitMQ topology generator')
    parser.add_argument('-i', '--infile',
                        type=argparse.FileType('r'),
                        required=True,
                        help='Broker definition file')
    parser.add_argument('-o', '--outfile',
                        type=argparse.FileType('w'),
                        required=True,
                        help='Output file')

    return parser.parse_args()

def gen():
    ''' Generator '''
    args = parse_args()
    broker = Broker(json.loads(args.infile.read()))

    # Create graph
    graph = pgv.AGraph(directed=True, strict=False)

    for exchange in broker.exchanges():
        graph.add_node(exchange.name, shape="square")

    for queue in broker.queues():
        graph.add_node(queue.name, shape="rectangle")

    for binding in broker.bindings():
        graph.add_edge(binding.source, binding.destination, label=binding.routing_key)
        # print('{} --- {} --- {}'.format(binding.source, binding.routing_key, binding.destination))

    for policy in broker.policies():
        if policy.pattern is not None and policy.definition.dead_letter_exchange is not None:
            graph.add_edge(policy.pattern, policy.definition.dead_letter_exchange,
                           label=policy.definition.dead_letter_routing_key)

    # graph.layout(prog='circo')
    # graph.write(args.outfile)
    graph.draw(args.outfile.name, prog='circo')

gen()
