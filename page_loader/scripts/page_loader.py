#!/usr/bin/env python
import argparse
from pathlib import Path
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', nargs='?', default=Path.cwd(),
                        help='output directory (default: "current directory")')
    args = parser.parse_args()
    print(download(args.url, args.output))


if __name__ == '__main__':
    main()
