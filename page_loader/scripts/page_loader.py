import argparse
import sys
from pathlib import Path
from page_loader import download


def main():
    parser = argparse.ArgumentParser(description='Download page')
    parser.add_argument('url', type=str)
    parser.add_argument('-o', '--output', default=Path.cwd(),
                        help='output directory (default: "current directory")')
    args = parser.parse_args()

    try:
        print(download(args.url, args.output))
    except FileNotFoundError:
        sys.exit(1)
    except PermissionError:
        sys.exit(1)
    except ConnectionError:
        sys.exit(2)
    except Exception:
        sys.exit(3)


if __name__ == '__main__':
    main()
