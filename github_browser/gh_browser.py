from . import cmd_parser


def main(args):
    applicationContext = cmd_parser.parse(args)

    if applicationContext is None:
        print("No cmd specified")
    else:
        applicationContext.run()