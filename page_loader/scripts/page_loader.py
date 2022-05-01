import argparse
import sys
from pathlib import Path
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', nargs='?', default=Path.cwd(),
                        help='output directory (default: "current directory")')
    args = parser.parse_args()

    try:
        print(download(args.url, args.output))
    except FileNotFoundError:
        sys.exit("This folder does not exist or wrong path")
    except PermissionError:
        sys.exit("No permission to create folder")
    except OSError:
        sys.exit("Error connection")


if __name__ == '__main__':
    main()
