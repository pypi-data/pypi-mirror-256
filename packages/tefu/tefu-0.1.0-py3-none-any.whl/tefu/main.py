import argparse


def init(args):
    print("add")


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_add = subparsers.add_parser("init", help="initialize")
# parser_add.add_argument('-A', '--all', action='store_true', help='all files')
parser_add.set_defaults(handler=init)

args = parser.parse_args()

if hasattr(args, "handler"):
    args.handler(args)
else:
    print("defalut")
