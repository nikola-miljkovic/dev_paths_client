from . import cmd_parser


def main(args):
    application_context = cmd_parser.parse(args)

    if application_context is not None:
        application_context.run()

        if hasattr(application_context, 'get_sanitized_data'):
            print(application_context.get_sanitized_data())
        elif hasattr(application_context, 'get_data_stream'):
            for output in application_context.get_data_stream():
                print(output)