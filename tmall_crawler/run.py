import sys
import argparse

from multiprocessing import Process
from tmall_crawler.tasks import run

parser = argparse.ArgumentParser(description='tmall site clone')

parser.add_argument('-s', '--site', action='append', required=True)
parser.add_argument('-d', '--dir', action='append')
parser.add_argument('-c', '--celery', action='store_true')


def main():
    args = parser.parse_args()
    sites = args.site
    dirs = args.dir

    ps = []
    for idx, site in enumerate(sites):
        if dirs:
            if idx < len(dirs):
                path = dirs[idx]
            else:
                path = None
        else:
            path = None
        if args.celery:
            run.delay(site, path)
        else:
            ps.append(Process(target=run, args=(site, path,)))

    if args.celery:
        return

    for p in ps:
        p.start()
    for p in ps:
        p.join()


if __name__ == '__main__':
    main()
