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

def main():
    ''' Generator '''
    args = parse_args()
    broker = Broker(json.loads(args.infile.read()))
    args.infile.close()

    # Create graph
    graph = pgv.AGraph(directed=True, strict=False, rankdir='LR')
    exchanges = [exchange.name for exchange in broker.exchanges()]
    queues = [queue.name for queue in broker.queues()]

    for exchange in exchanges:
        graph.add_node(exchange, shape='square', color='#3333CC')

    for queue in queues:
        graph.add_node(queue, shape='rectangle', color='#FF0000')

    for binding in broker.bindings():
        graph.add_edge(binding.source, binding.destination, label=binding.routing_key,
                       group=binding.source)

    for policy in broker.policies():
        if policy.pattern is not None and policy.definition.dead_letter_exchange is not None:
            graph.add_edge(policy.pattern, policy.definition.dead_letter_exchange,
                           label=policy.definition.dead_letter_routing_key, group=policy.pattern)

    # graph.layout(prog='dot')
    # graph.write(args.outfile)
    graph.draw(args.outfile.name, prog='dot')
    args.outfile.close()


if __name__ == "__main__":
    main()
