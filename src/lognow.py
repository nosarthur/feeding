import argparse


def add_weight(args):
    args


def add_feed(args):
    args


def add_stool(args):
    args


def show(args):
    args


def main(argv=None):
    p = argparse.ArgumentParser(prog='lognow')
    subparsers = p.add_subparsers(title='sub-commands')

    p_weight = subparsers.add_parser('weight', help='add weight')
    p_weight.add_argument('weight', type=float, help='in kg')
    p_weight.set_defaults(func=add_weight)

    p_feed = subparsers.add_parser('feed', help='add feeding')
    p_feed.add_argument('volume', type=float, help='in oz')
    p_feed.add_argument('-formula', action='store_true', help='formula is fed')
    p_feed.set_defaults(func=add_feed)

    p_stool = subparsers.add_parser('stool', help='add stool count')
    p_stool.add_argument('count', type=int, default=1, help='stool count')
    p_stool.set_defaults(func=add_stool)

    p_show = subparsers.add_parser('show', help='show log')
    p_show.add_argument('date', nargs='?', help='')
    p_show.set_defaults(func=show)


    args = p.parse_args(argv)
    print(args)

    if 'func' in args:
        args.func(args)
    else:
        p.print_help()  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
