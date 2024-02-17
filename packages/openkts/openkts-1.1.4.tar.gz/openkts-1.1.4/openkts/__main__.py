import argparse
import sys

import common
import version

class ArgParser(argparse.ArgumentParser):
    """
    argparse ArgumentParser internal override for custom help functionality
    """
    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        message = f" • split:\n\tpython3 \"{ sys.argv[0] }\" split -f STRING -m INT -n INT -e\n\n\t-f: Filepath to file to be split into shares.\n\t-m: Minimum number of shares needed to reconstruct the file.\n\t-n: Total number of shares to split the file into.\n\t-e: OPTIONAL - Password encrypt shares if provided.\n\n • join:\n\tpython3 \"{ sys.argv[0] }\" join -s STRING -o STRING -d\n\n\t-s: REPEATABLE - Filepath to a share of the file to be reconstucted.\n\t-o: OPTIONAL - Output file path\n\t-d: OPTIONAL - Password decrypt shares if provided."
        file.write(message+"\n")

if (__name__ == "__main__"):
    print("\n============================================")
    print(f"  Open Keyshare Threshold Scheme - CLI: v{version.VERSION}")
    print("============================================\n")

    parser = ArgParser()
    subparsers = parser.add_subparsers()

    split_parser = subparsers.add_parser("split")
    split_parser.add_argument("-f", action="store", required=True)
    split_parser.add_argument("-m", action="store", type=int, required=True)
    split_parser.add_argument("-n", action="store", type=int, required=True)
    split_parser.add_argument("-e", action="store_true")

    join_parser = subparsers.add_parser("join")
    join_parser.add_argument("-s", action="append", required=True)
    join_parser.add_argument("-o", action="store")
    join_parser.add_argument("-d", action="store_true")

    args = vars(parser.parse_args())

    try:
        if 'f' in args and 'm' in args and 'n' in args:
            common.split(args)
        elif 's' in args:
            common.join(args)
    except Exception as error:
        if "Invalid base64-encoded string" in str(error):
            print(f"\n An error occurred: File is not encrypted")
        else:
            if len(str(error)) > 0:
                print(f"\n An error occurred: {error}")
            else:
                print(f"\n An error occurred: {sys.exc_info()}")