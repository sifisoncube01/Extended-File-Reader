import sys
import os
import csv
import json
import pickle
from abc import ABC, abstractmethod


class FileHandler(ABC):

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst
        self.data = []

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

    def display(self):
        print("\nModified file content:")
        for row in self.data:
            print(','.join(map(str, row)))

    def apply_changes(self, changes):
        for change in changes:
            try:
                parts = change.split(',')
                if len(parts) != 3:
                    raise ValueError(f"Invalid format: {change}. Expected 'col,row,value'.")
                col, row, value = int(parts[0]), int(parts[1]), parts[2]

                if row < 0 or row >= len(self.data):
                    raise IndexError(f"Row {row} out of range.")
                if col < 0 or col >= len(self.data[row]):
                    raise IndexError(f"Column {col} out of range.")

                self.data[row][col] = value
            except Exception as e:
                print(f"Skipping change '{change}': {e}")

class CSVHandler(FileHandler):
    def read(self):
        with open(self.src, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            self.data = [row for row in reader]

    def write(self):
        with open(self.dst, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.data)
        print(f"\nModified CSV saved to: {self.dst}")


class JSONHandler(FileHandler):
    def read(self):
        with open(self.src, 'r', encoding='utf-8') as jsonfile:
            self.data = json.load(jsonfile)

    def write(self):
        with open(self.dst, 'w', encoding='utf-8') as jsonfile:
            json.dump(self.data, jsonfile, indent=4)
        print(f"\nModified JSON saved to: {self.dst}")


class PickleHandler(FileHandler):
    def read(self):
        with open(self.src, 'rb') as pklfile:
            self.data = pickle.load(pklfile)

    def write(self):
        with open(self.dst, 'wb') as pklfile:
            pickle.dump(self.data, pklfile)
        print(f"\nModified Pickle saved to: {self.dst}")


def list_files_in_directory(directory):
    print("Files in directory:")
    try:
        for f in os.listdir(directory):
            print(f)
    except Exception as e:
        print(f"Could not list files: {e}")


def get_handler(src, dst):
    ext = os.path.splitext(src)[1].lower()

    if ext == '.csv':
        return CSVHandler(src, dst)
    elif ext == '.json':
        return JSONHandler(src, dst)
    elif ext == '.pickle':
        return PickleHandler(src, dst)
    else:
        print(f"Unsupported file type: {ext}")
        sys.exit(1)


def main():
    if len(sys.argv) < 3:
        print("Usage: python reader.py <src> <dst> <change1> <change2> ...")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    changes = sys.argv[3:]

    if not os.path.isfile(src):
        print(f"Error: Source file '{src}' does not exist or is not a file.")
        directory = os.path.dirname(src) or '.'
        list_files_in_directory(directory)
        sys.exit(1)

    handler = get_handler(src, dst)

    handler.read()
    handler.apply_changes(changes)
    handler.display()
    handler.write()


if __name__ == "__main__":
    main()
