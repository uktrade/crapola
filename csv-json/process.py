import json
import argparse
import csv


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('csv')
    args = arg_parser.parse_args()

    with open(args.csv, 'r') as csv_fh:
        row_dicts = [row_dict for row_dict in csv.DictReader(csv_fh)]

    print(json.dumps(row_dicts, indent=2))
