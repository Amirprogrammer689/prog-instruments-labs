import argparse
import sys
import time

from Asymmetric import Asymmetric
from Symmetric import SymmetricCryptography
from read_or_write_files import *


def loading_animation():
    """
    Display a loading animation with progress bar.

    This function displays a loading animation with a progress bar that fills up as the loading progresses.
    The progress bar changes from '▢' to '▣' as the loading reaches completion.
    Upon completion, it prints a message 'Loading completed!' in red color with a smiling face emoji.
    """
    toolbar_width = 40
    sys.stdout.write("Loading: ")
    sys.stdout.flush()

    progress_bar = '▢' * toolbar_width
    sys.stdout.write(f"\r\033[38;5;27mLoading: 0% \033[0m\033[38;5;40m{progress_bar}\033[0m")
    sys.stdout.flush()

    for i in range(1, 101):
        time.sleep(0.1)
        progress_bar = '▢' * (toolbar_width * i // 100)
        sys.stdout.write(
            f"\r\033[38;5;27mLoading: {i}% \033[0m\033[38;5;40m{progress_bar.replace('▢', '▣')}\033[0m"
        )
        sys.stdout.flush()

    progress_bar_final = '▣' * toolbar_width
    sys.stdout.write(f"\r\033[38;5;27mLoading: 100% \033[0m\033[38;5;40m{progress_bar_final}\033[0m")
    sys.stdout.write("\n")
    print("\033[91mLoading completed! \U0001F60A\033[0m")


def menu():
    """
    Displays a menu for selecting various cryptographic operations.

    This feature provides a menu with options for generating keys, encrypting and decrypting files.
    It reads paths from a JSON file, parses command line arguments.
    """
    parser = argparse.ArgumentParser()
    paths = read_json_from_file("path.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', help='Generate symmetric and asymmetric keys')
    group.add_argument('-enc', '--encryption', help='Encrypt a file using symmetric key')
    group.add_argument('-dec', '--decryption', help='Decrypt a file using symmetric key')
    group.add_argument('-enc_sym', '--encryption_symmetric', help='Encrypt sym key using asym encryption')
    group.add_argument('-dec_sym', '--decryption_symmetric', help='Decrypt sym key using asym decryption')
    parser.add_argument("path", type=str, help="File path")

    args = parser.parse_args()

    sym = SymmetricCryptography()
    asym = Asymmetric()

    match args:
        case args if args.generation:
            key_choice = input("\033[91;107mDo you want to use a custom symmetric key? (yes/no):\033[0;92m ")
            if key_choice.lower() == 'yes':
                custom_key_path = input("\033[91;107mEnter the path to your custom symmetric key file:\033[0;92m ")
                sym.load_custom_key(custom_key_path)
            else:
                key_length = int(input(
                    "\033[91;107mEnter the key length in bits, in the range [128, 192, 256]:\033[0;92m "
                ))
                print(f"\033[91;107mYour key length:\033[0;95m {key_length} \033[0m")
                loading_animation()
                asym.generate_keys()
                asym.serialization_private(paths["secret_key_path"])
                asym.serialization_public(paths["public_key_path"])
                sym.generation_key(key_length)
                sym.save_generated_key(paths["symmetric_key_path"])
        case args if args.encryption:
            sym.key_deserialization(paths["symmetric_key_path"])
            sym.encrypt(paths["initial_file_path"], paths["encrypted_file_path"])
        case args if args.decryption:
            sym.key_deserialization(paths["symmetric_key_path"])
            sym.decrypt(paths["encrypted_file_path"], paths["decrypted_file_path"])
        case args if args.encryption_symmetric:
            sym.key_deserialization(paths["symmetric_key_path"])
            asym.public_key_deserialization(paths["public_key_path"])
            symmetric_key = sym.key
            encrypted_symmetric_key = asym.encrypt(symmetric_key)
            write_binary_to_file(paths["encrypted_key_path"], encrypted_symmetric_key)
        case args if args.decryption_symmetric:
            sym.key_deserialization(paths["symmetric_key_path"])
            asym.private_key_deserialization(paths["secret_key_path"])
            encrypted_symmetric_key = read_binary_from_file(paths["encrypted_key_path"])
            decrypted_symmetric_key = asym.decrypt(encrypted_symmetric_key)
            write_binary_to_file(paths["decrypted_key_path"], decrypted_symmetric_key)


if __name__ == "__main__":
    menu()
