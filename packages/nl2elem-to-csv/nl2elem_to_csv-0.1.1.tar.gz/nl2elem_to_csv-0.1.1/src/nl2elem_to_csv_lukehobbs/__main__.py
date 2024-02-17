import argparse

import nl2elem_reader
import data_processor
import csv_writer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', type=str, required=False, default='track.nl2elem')
    parser.add_argument('--output', '-o', type=str, required=False, default='track.csv')
    args = parser.parse_args()

    data = None
    with open(args.input, 'rb') as file:
        data = nl2elem_reader.read(file)

    processed_data = data_processor.process_data(data)
    print(processed_data)

    csv_writer.write_to_csv(processed_data, args.output)


if __name__ == '__main__':
    main()
