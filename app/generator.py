import argparse
import json

from broker import Broker


parser = argparse.ArgumentParser(description='RabbitMQ topology generator')
parser.add_argument('-i', '--infile', type=argparse.FileType('r'), required=True, help='Broker definition file')
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), required=True, help='Output .dot file')
args = parser.parse_args()

broker = Broker(json.loads(args.infile.read()))


for e in broker.exchange_names():
    print(e)
