import argparse
from github_browser.application_context import ListApplicationContext, DescApplicationContext

def add_narg(parser, _nargs = 1, _default = 20):
    parser.add_argument('-n', nargs=_nargs, default=_default, type=int)

def parse(args):
    parser = argparse.ArgumentParser(description='TODO')
    subparsers = parser.add_subparsers(help="Commands")

    parser_list = subparsers.add_parser('list', help="Lists repositories")
    parser_list.set_defaults(which='list')
    parser_list.add_argument('lang', nargs='?', default=None, help='ruby')
    parser_list.add_argument('-s', '--sort', nargs='?', default='updated', choices=['updated', 'stars', 'forks'])
    add_narg(parser_list)

    parser_desc = subparsers.add_parser('desc', help="Lists repositories")
    parser_desc.set_defaults(which='desc')
    add_narg(parser_desc)

    try:
        parser = parser.parse_args(args)
    except:
        parser.print_usage()
        return None

    # parse_args makes list instead of single integer value for n,
    # so we need to check if that is case and set proper value
    if hasattr(parser, 'n') and isinstance(parser.n, list):
        parser.n = parser.n[0]

    if not hasattr(parser, 'which'):
        return None
    elif parser.which is 'desc':
        return DescApplicationContext(parser.n)
    elif parser.which is 'list':
        return ListApplicationContext(parser.n, lang=parser.lang, sort=parser.sort)
