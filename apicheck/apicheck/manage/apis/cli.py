

def cli(parser):

    proxy_args = parser.add_parser(
        'api',
        help='Manage stored APIs')
    proxy_args.add_argument('api_action',
                            default="list",
                            help="list stores APIs")
