import json


def write_text_to_file(file_path: str, text: str) -> None:
    """
    Write text data to a file.
    Parameters:
    file_path (str): The path to the file to write.
    text (str): The text to write to the file.
    """
    try:
        with open(file_path, 'a+', encoding='utf-8') as file:
            file.write(text)
        print("\033[91;107mThe information is successfully saved to the file.\033[0m")
    except FileNotFoundError as e:
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except Exception as e:
        print(f"\033[97;41mAn error occurred while writing to the file: {e}\033[0m")


def read_json_from_file(file_path: str) -> dict:
    """
    Read JSON data from a file.
    Parameters:
    file_path (str): The path to the JSON file to read.
    Returns:
    dict: The JSON data read from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError as e:
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except json.JSONDecodeError as e:
        print(f"\033[97;41mError while decoding JSON: {e}\033[0m")
    except Exception as e:
        print(f"\033[97;41mAn error has occurred: {e}\033[0m")


def read_binary_from_file(file_path: str) -> bytes:
    """
    Read binary data from a file.
    Parameters:
    file_path (str): The path to the file to read.
    Returns:
    bytes: The binary data read from the file.
    """
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        return data
    except FileNotFoundError as e:
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except Exception as e:
        print(f"\033[97;41mAn error occurred while reading the file: {e}\033[0m")


def write_binary_to_file(file_path: str, bytes_text: bytes) -> None:
    """
    Write binary data to a file.
    Parameters:
    file_path (str): The path to the file to write.
    bytes_text (bytes): The binary data to write to the file.
    """
    try:
        with open(file_path, 'wb') as file:
            file.write(bytes_text)
        print("\033[91;107mThe binary data has been successfully saved to the file.\033[0m")
    except FileNotFoundError as e:
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except Exception as e:
        print(f"\033[97;41mAn error occurred while writing the binary data to the file: {e}\033[0m")
