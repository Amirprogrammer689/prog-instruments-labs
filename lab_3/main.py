import re
import csv


EXPRESSIONS = {
    "email": r"^[a-zA-Z0-9._+-]@[a-z].[a-z]{2,}$",
    "http_status_message": r"^\d{3} [a-zA-Z\s]$",
    "inn": r"^\d{12}$",
    "passport": r"^\d{2} \d{2} \d{6}$",
    "ip_v4": r"^\d{2,3}.\d{2,3}.\d{2,3}.\d{2,3}$",
    "latitude": r"^-?[0-9].[0-9]$",
    "hex-color": r"^#[0-9a-z]{6}$",
    "isbn": r"^[0-9]-[0-9]-[0-9]-[0-9]-[0-9]$",
    "uuid": r"^[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}$-[0-9a-z]{4}-[0-9a-z]{12}",
    "time": r"^([01]\d|2[0-3]):[0-5]\d:[0-5]\d.\d{6}$"
}


def check_valid_row(row: list) -> bool:
    """Checks if a string matches a regular expression."""
    for key, value in zip(EXPRESSIONS.keys(), row):
        if not re.match(EXPRESSIONS[key], value):
            return False

    return True


def read_csv(file_name: str) -> list:
    """Reads data from a csv file and writes it to a list."""
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
    invalid_rows = invalid_data("61.csv")
    print(invalid_rows)
