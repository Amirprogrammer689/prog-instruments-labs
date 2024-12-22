import os
import logging

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from read_or_write_files import read_binary_from_file, write_binary_to_file, write_text_to_file


logger = logging.getLogger(__name__)


class SymmetricCryptography:
    """
    A class for symmetric cryptography operations.
    """

    def __init__(self):
        self.key = None
        logger.info("SymmetricCryptography instance created.")

    def generation_key(self, size_key: int) -> bytes:
        """
        Generate a symmetric encryption key.

        Parameters:
        size_key (int): The size of the key in bits (128, 192, or 256).

        Returns:
        bytes: The generated key.
        """
        logger.info(f"Generating symmetric key with size: {size_key} bits.")
        if size_key not in [128, 192, 256]:
            logger.error(f"Invalid key length: {size_key}. Please choose 128, 192, or 256 bits.")
            raise ValueError("Invalid key length. Please choose 128, 192, or 256 bits.")

        self.key = os.urandom(size_key // 8)
        logger.info("Symmetric key generated successfully.")
        return self.key

    def load_custom_key(self, path: str) -> None:
        """
        Load a custom symmetric key from a file.

        Parameters:
        path (str): The path to the file containing the custom key.
        """
        logger.info(f"Loading custom key from: {path}")
        try:
            with open(path, 'rb') as key_file:
                self.key = key_file.read()
            logger.info(f"Custom key loaded from {path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during custom key loading: {e}")

    def save_generated_key(self, path: str) -> None:
        """
        Save the generated symmetric key to a file.

        Parameters:
        path (str): The path to save the generated key.
        """
        logger.info(f"Saving generated key to: {path}")
        try:
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
            logger.info(f"Generated key saved to {path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during key saving: {e}")

    def key_serialization(self, path: str) -> None:
        """
        Serialize the encryption key to a file.

        Parameters:
        path (str): The path to save the key.
        """
        logger.info(f"Serializing key to: {path}")
        try:
            with open(path, 'wb') as key_file:
                key_file.write(self.key)
            logger.info(f"Key serialized to {path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during key serialization: {e}")

    def key_deserialization(self, path: str) -> None:
        """
        Deserialize the encryption key from a file.

        Parameters:
        path (str): The path to read the key from.
        """
        logger.info(f"Deserializing key from: {path}")
        try:
            with open(path, "rb") as file:
                self.key = file.read()
            logger.info(f"Key deserialized from {path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during key deserialization: {e}")

    def encrypt(self, path: str, encrypted_path: str) -> bytes:
        """
        Encrypt a file using the stored key and save the encrypted data to a new file.

        Parameters:
        path (str): The path to the file to encrypt.
        encrypted_path (str): The path to save the encrypted data.

        Returns:
        bytes: The encrypted data.
        """
        logger.info(f"Encrypting file: {path} and saving to {encrypted_path}")
        try:
            text = read_binary_from_file(path)
            iv = os.urandom(16)
            cipher = Cipher(algorithms.Camellia(self.key), modes.CBC(iv), backend=default_backend())
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            padded_text = padder.update(text) + padder.finalize()
            cipher_text = iv + encryptor.update(padded_text) + encryptor.finalize()
            write_binary_to_file(encrypted_path, cipher_text)
            logger.info(f"File encrypted and saved to {encrypted_path} successfully.")
            return cipher_text
        except Exception as e:
            logger.error(f"An error occurred during encryption: {e}")
            return b""

    def decrypt(self, encrypted_path: str, decrypted_path: str) -> str:
        """
        Decrypt an encrypted file using the stored key and save the decrypted data to a new file.

        Parameters:
        encrypted_path (str): The path to the encrypted file.
        decrypted_path (str): The path to save the decrypted data.

        Returns:
        str: The decrypted text.
        """
        logger.info(f"Decrypting file: {encrypted_path} and saving to {decrypted_path}")
        try:
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
            logger.info(f"File decrypted and saved to {decrypted_path} successfully.")
            return decrypt_text
        except Exception as e:
            logger.error(f"An error occurred during decryption: {e}")
            return ""


if __name__ == '__main__':
    import log_config
    log_config.configure_logging()
    logger.info("Starting the main application")
    symmetric_crypto = SymmetricCryptography()
    symmetric_crypto.generation_key(256)
    symmetric_crypto.save_generated_key('key.bin')
    symmetric_crypto.key_deserialization('key.bin')

    with open('test.txt', 'w') as f:
        f.write("This is a test text for encryption.")

    symmetric_crypto.encrypt('test.txt', 'test.enc')
    symmetric_crypto.decrypt('test.enc', 'test_dec.txt')
    logger.info("Application finished successfully")
