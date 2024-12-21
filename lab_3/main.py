import csv
import re

from checksum import calculate_checksum, serialize_result

PATTERNS = {
    "email": r"^[a-zA-Z0-9._+-]+@[a-z]+\.[a-z]{2,}$",
    "http_status_message": r"^\d{3}( [a-zA-Z]{2,}){1,}$",
    "inn": r"^\d{12}$",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "ip_v4": r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.){3}(25[0-5]|(2[0-4]|1\d|[1-9]|)\d)$",
    "latitude": r"^[-]?(90(\.0+)?|[1-8]?\d(\.\d+)?|0?\.\d+)$",
    "hex-color": r"^#[0-9a-fA-F]{6}$",
    "isbn": r"^(?:ISBN(?:-1[03])?: )?(?:\d{9}[\dX]|\d{3}-\d-\d{2}-\d{6}-[\dX])$",
    "uuid": r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
    "time": r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d\.\d{6}$"
}


def check_valid_row(row: list) -> bool:
    """Checks if a string matches a regular expression."""
    for key, value in zip(PATTERNS.keys(), row):
        if not re.match(PATTERNS[key], value):
            return False

    return True


def read_csv(file_name: str) -> list:
    """Reads data from a CSV file and writes it to a list."""
    with open(file_name, "r", newline="", encoding="utf-16") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)
        return list(reader)


def invalid_data(path_csv: str) -> list:
    """Writes line numbers that do not match regular expressions."""
    data = read_csv(path_csv)
    invalid_rows_numbers = []

    for i in range(len(data)):
        if not check_valid_row(data[i]):
            invalid_rows_numbers.append(i)

    return invalid_rows_numbers


if __name__ == "__main__":
    variant = 61
    invalid_rows = invalid_data("61.csv")
    serialize_result(variant, calculate_checksum(invalid_rows))
