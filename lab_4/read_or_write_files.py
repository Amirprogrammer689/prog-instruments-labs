import json
import logging


logger = logging.getLogger(__name__)


def write_text_to_file(file_path: str, text: str) -> None:
    """
    Write text data to a file.
    Parameters:
    file_path (str): The path to the file to write.
    text (str): The text to write to the file.
    """
    logger.info(f"Writing text to file: {file_path}")
    try:
        with open(file_path, 'a+', encoding='utf-8') as file:
            file.write(text)
        logger.info(f"Text successfully written to file: {file_path}")
        print("\033[91;107mThe information is successfully saved to the file.\033[0m")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except Exception as e:
        logger.error(f"An error occurred while writing to the file: {e}")
        print(f"\033[97;41mAn error occurred while writing to the file: {e}\033[0m")


def read_json_from_file(file_path: str) -> dict:
    """
    Read JSON data from a file.
    Parameters:
    file_path (str): The path to the JSON file to read.
    Returns:
    dict: The JSON data read from the file.
    """
    logger.info(f"Reading JSON from file: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.info(f"JSON data successfully read from file: {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\033[97;41mFile not found: {e}\033[0m")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"Error while decoding JSON: {e}")
        print(f"\033[97;41mError while decoding JSON: {e}\033[0m")
        return {}
    except Exception as e:
        logger.error(f"An error has occurred: {e}")
        print(f"\033[97;41mAn error has occurred: {e}\033[0m")
        return {}


def read_binary_from_file(file_path: str) -> bytes:
    """
    Read binary data from a file.
    Parameters:
    file_path (str): The path to the file to read.
    Returns:
    bytes: The binary data read from the file.
    """
    logger.info(f"Reading binary data from file: {file_path}")
    try:
        with open(file_path, 'rb') as file:
            data = file.read()
        logger.info(f"Binary data successfully read from file: {file_path}")
        return data
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\033[97;41mFile not found: {e}\033[0m")
        return b""
    except Exception as e:
        logger.error(f"An error occurred while reading the file: {e}")
        print(f"\033[97;41mAn error occurred while reading the file: {e}\033[0m")
        return b""


def write_binary_to_file(file_path: str, bytes_text: bytes) -> None:
    """
    Write binary data to a file.
    Parameters:
    file_path (str): The path to the file to write.
    bytes_text (bytes): The binary data to write to the file.
    """
    logger.info(f"Writing binary data to file: {file_path}")
    try:
        with open(file_path, 'wb') as file:
            file.write(bytes_text)
        logger.info(f"Binary data successfully written to file: {file_path}")
        print("\033[91;107mThe binary data has been successfully saved to the file.\033[0m")
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        print(f"\033[97;41mFile not found: {e}\033[0m")
    except Exception as e:
        logger.error(f"An error occurred while writing the binary data to the file: {e}")
        print(f"\033[97;41mAn error occurred while writing the binary data to the file: {e}\033[0m")
