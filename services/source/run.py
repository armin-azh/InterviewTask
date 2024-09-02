from argparse import ArgumentParser, Namespace

def main(args: Namespace)->None:

    pass


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-gpu', help='Enable on gpu', action='store_true')
    parser.add_argument('-host', help='Host name', type=str, default='0.0.0.0')
    parser.add_argument('-port', help='Server Port number', type=int, default=8081)
    main(parser.parse_args())