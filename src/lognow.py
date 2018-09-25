import argparse
import os
import pandas as pd
import numpy as np
from datetime import datetime

import utils


def add_weight(args):
    args


def add_feed(args):
    now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    with open(utils.fullpath('feed.csv'), 'a') as f:
        f.write(f'{now},{args.volume},{int(not args.formula)}')


def add_stool(args):
    today = datetime.today().strftime('%Y-%m-%d')
    with open(utils.fullpath('weight_stool.csv'), 'r+') as f:
        lines = f.readlines()
        last_day, last_weight, count = lines[-1].split(',')
        if last_day == today:
            update = f'{today},{last_weight},{int(count)+1}'
            lines[-1] = update
            f.seek(0, os.SEEK_SET)
            f.writelines(lines)
        else:
            f.write(f'{today},,1')


def show(args):
    with open(utils.fullpath('weight_stool.csv'), 'r') as f:
        print('stool:')
        for line in f.readlines()[-args.days:]:
            print(line, end='')

    df = utils.load_feedings()
    by_date = pd.pivot_table(
        df,
        values='Vol',
        index=df.index.date,
        columns=['BM'],
        aggfunc=np.sum,
        fill_value=0)
    print(by_date.tail(args.days))


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
    p_stool.set_defaults(func=add_stool)

    p_show = subparsers.add_parser('show', help='show log')
    p_show.add_argument('days', nargs='?', type=int, default=1, help='')
    p_show.set_defaults(func=show)

    args = p.parse_args(argv)
    print(args)

    if 'func' in args:
        args.func(args)
    else:
        p.print_help()  # pragma: no cover


if __name__ == '__main__':
    main()  # pragma: no cover
