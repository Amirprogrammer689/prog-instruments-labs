import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from read_or_write_files import *


class SymmetricCryptography:
    """
    A class for symmetric cryptography operations.
    """
    def __init__(self):
        self.key = None

    def generation_key(self, size_key: int) -> bytes:
        """
        Generate a symmetric encryption key.

        Parameters:
        size_key (int): The size of the key in bits (128, 192, or 256).

        Returns:
        bytes: The generated key.
        """
        if size_key not in [128, 192, 256]:
            raise ValueError("Invalid key length. Please choose 128, 192, or 256 bits.")

        self.key = os.urandom(size_key // 8)
        return self.key

    def load_custom_key(self, path: str) -> None:
        """
        Load a custom symmetric key from a file.

        Parameters:
        path (str): The path to the file containing the custom key.
        """
        try:
            with open(path, 'rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def save_generated_key(self, path: str) -> None:
        """
        Save the generated symmetric key to a file.

        Parameters:
        path (str): The path to save the generated key.
        """
        try:
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def key_serialization(self, path: str) -> None:
        """
        Serialize the encryption key to a file.

        Parameters:
        path (str): The path to save the key.
        """
        try:
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def key_deserialization(self, path: str) -> None:
        """
        Deserialize the encryption key from a file.

        Parameters:
        path (str): The path to read the key from.
        """
        try:
            with open(path, "rb") as file:
                self.key = file.read()
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def encrypt(self, path: str, encrypted_path: str) -> bytes:
        """
        Encrypt a file using the stored key and save the encrypted data to a new file.

        Parameters:
        path (str): The path to the file to encrypt.
        encrypted_path (str): The path to save the encrypted data.

        Returns:
        bytes: The encrypted data.
        """
        text = read_binary_from_file(path)
        iv = os.urandom(16)
        cipher = Cipher(algorithms.Camellia(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_text = padder.update(text) + padder.finalize()
        cipher_text = iv + encryptor.update(padded_text) + encryptor.finalize()
        write_binary_to_file(encrypted_path, cipher_text)
        return cipher_text

    def decrypt(self, encrypted_path: str, decrypted_path: str) -> str:
        """
        Decrypt an encrypted file using the stored key and save the decrypted data to a new file.

        Parameters:
        encrypted_path (str): The path to the encrypted file.
        decrypted_path (str): The path to save the decrypted data.

        Returns:
        str: The decrypted text.
        """
        encrypted_text = read_binary_from_file(encrypted_path)
        iv = encrypted_text[:16]
        cipher_text = encrypted_text[16:]
        cipher = Cipher(algorithms.Camellia(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypt_text = decryptor.update(cipher_text) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        unpadded_dc_text = unpadder.update(decrypt_text) + unpadder.finalize()
        decrypt_text = unpadded_dc_text.decode('utf-8')
        write_text_to_file(decrypted_path, decrypt_text)
        return decrypt_text
