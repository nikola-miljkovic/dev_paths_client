import argparse

from github_browser.application_context import ListApplicationContext, DescApplicationContext, LatestApplicationContext

HELP_LIST = "Lists latest repository with applied filters"
HELP_DESC = "Shows info on requested repositories"
HELP_LATEST = "Shows name of newest repository"


def parse(args):
    parser = argparse.ArgumentParser(prog='ghtool', description='Provides data and information from GitHub')
    subparsers = parser.add_subparsers(help="Available commands")

    parser_list = subparsers.add_parser('list', help=HELP_LIST, description=HELP_LIST)
    parser_list.set_defaults(which='list')
    parser_list.add_argument('lang', nargs='?', default=None, help='Language filter, e.g. assembly, ruby...')
    parser_list.add_argument('-s', '--sort', nargs='?', default='default',
                             choices=['updated', 'stars', 'forks', 'default'],
                             help='Octopus API supported sorts or "default", custom sort by "created_at" field')
    parser_list.add_argument('-n', nargs=1, default=20, type=int, help='Maximum entries to display')
    parser_list.add_argument('-t', action='store_true', help='Improves output format, shows #num and date')

    parser_desc = subparsers.add_parser('desc', help=HELP_DESC, description=HELP_DESC)
    parser_desc.set_defaults(which='desc')
    parser_desc.add_argument('id', nargs='+', help='List of ids, default github id is <owner>/<repo_name> e.g. '
                                                   'nikola-miljkovic/Github_PROJ')

    parser_latest = subparsers.add_parser('latest', help=HELP_LATEST, description=HELP_LATEST)
    parser_latest.set_defaults(which='latest')

    try:
        parser = parser.parse_args(args)
    except:
        return None

    # parse_args makes list instead of single integer value for n,
    # so we need to check if that is case and set proper value
    if hasattr(parser, 'n') and isinstance(parser.n, list):
        parser.n = parser.n[0]

    if not hasattr(parser, 'which'):
        return None
    elif parser.which is 'desc':
        return DescApplicationContext(parser.id)
    elif parser.which is 'list':
        return ListApplicationContext(parser.n, lang=parser.lang, sort=parser.sort, extended_output=parser.t)
    elif parser.which is 'latest':
        return LatestApplicationContext()
