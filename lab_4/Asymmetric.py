import logging

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


logger = logging.getLogger(__name__)


class Asymmetric:
    """
    A class that implements asymmetric encryption and decryption using the RSA algorithm.

    Attributes
    private_key: The private key.
    public_key: The public key.
    """

    def __init__(self):
        self.private_key = None
        self.public_key = None
        logger.info("Asymmetric instance created.")

    def generate_keys(self) -> None:
        """
        Generate RSA private and public keys.
        """
        logger.info("Generating RSA keys.")
        keys = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.private_key = keys
        self.public_key = keys.public_key()
        logger.info("RSA keys generated successfully.")

    def serialization_public(self, public_path: str) -> None:
        """
        Serialize the public key to a file.

        Parameters:
        public_path (str): The path to save the public key.
        """
        logger.info(f"Serializing public key to: {public_path}")
        public_key = self.public_key
        try:
            with open(public_path, 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo
                                                         )
                                 )
            logger.info(f"Public key serialized to {public_path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during public key serialization: {e}")

    def serialization_private(self, private_path: str) -> None:
        """
        Serialize the private key to a file.

        Parameters:
        private_path (str): The path to save the private key.
        """
        logger.info(f"Serializing private key to: {private_path}")
        private_key = self.private_key
        try:
            with open(private_path, 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()
                                                            )
                                  )
            logger.info(f"Private key serialized to {private_path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during private key serialization: {e}")

    def public_key_deserialization(self, public_path: str) -> None:
        """
        Deserialize the public key from a file.

        Parameters:
        public_path (str): The path to read the public key from.
        """
        logger.info(f"Deserializing public key from: {public_path}")
        try:
            with open(public_path, 'rb') as pem_in:
                public_bytes = pem_in.read()
            self.public_key = load_pem_public_key(public_bytes)
            logger.info(f"Public key deserialized from {public_path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during public key deserialization: {e}")

    def private_key_deserialization(self, private_path: str) -> None:
        """
        Deserialize the private key from a file.

        Parameters:
        private_path (str): The path to read the private key from.
        """
        logger.info(f"Deserializing private key from: {private_path}")
        try:
            with open(private_path, 'rb') as pem_in:
                private_bytes = pem_in.read()
            self.private_key = load_pem_private_key(private_bytes, password=None)
            logger.info(f"Private key deserialized from {private_path} successfully.")
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
        except Exception as e:
            logger.error(f"An error occurred during private key deserialization: {e}")

    def encrypt(self, symmetric_key: bytes) -> bytes:
        """
        Encrypts a symmetric key using the public key.
        Parameters
            symmetric_key (bytes): The symmetric key to be encrypted.
        Returns
            The encrypted symmetric key.
        """
        logger.info("Encrypting symmetric key.")
        encrypted_symmetric_key = self.public_key.encrypt(symmetric_key,
                                                          padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                       algorithm=hashes.SHA256(),
                                                                       label=None)
                                                          )
        logger.info("Symmetric key encrypted successfully.")
        return encrypted_symmetric_key

    def decrypt(self, encrypted_symmetric_key: bytes) -> bytes:
        """
        Decrypts an encrypted symmetric key using the private key.
        Parameters
            encrypted_symmetric_key (bytes): The encrypted symmetric key to be decrypted.
        Returns
            The decrypted symmetric key.
        """
        logger.info("Decrypting symmetric key.")
        try:
            decrypted_symmetric_key = self.private_key.decrypt(encrypted_symmetric_key,
                                                               padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                            algorithm=hashes.SHA256(),
                                                                            label=None)
                                                               )
            logger.info("Symmetric key decrypted successfully.")
            return decrypted_symmetric_key
        except Exception as e:
            logger.error(f"An error occurred during decryption: {e}")
            return b""


if __name__ == '__main__':
    import log_config
    log_config.configure_logging()
    asymmetric = Asymmetric()
    asymmetric.generate_keys()
    asymmetric.serialization_public('public.pem')
    asymmetric.serialization_private('private.pem')
    asymmetric.public_key_deserialization('public.pem')
    asymmetric.private_key_deserialization('private.pem')

    symmetric_key = b'This is my secret key'
    encrypted_key = asymmetric.encrypt(symmetric_key)
    decrypted_key = asymmetric.decrypt(encrypted_key)

    if symmetric_key == decrypted_key:
        print("Encryption and decryption successful!")
    else:
        print("Encryption and decryption failed!")
