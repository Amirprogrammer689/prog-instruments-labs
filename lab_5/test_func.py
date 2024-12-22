import os
import pytest

from unittest.mock import mock_open, patch
from Asymmetric import Asymmetric
from Symmetric import SymmetricCryptography
from read_or_write_files import read_json_from_file, write_text_to_file, read_binary_from_file, write_binary_to_file


# Test for Asymmetric class
def test_asymmetric_key_generation():
    asym = Asymmetric()
    asym.generate_keys()
    assert asym.public_key is not None
    assert asym.private_key is not None


def test_asymmetric_serialization_deserialization():
    asym = Asymmetric()
    asym.generate_keys()
    public_path = "test_public.pem"
    private_path = "test_private.pem"
    asym.serialization_public(public_path)
    asym.serialization_private(private_path)

    asym_deserialized = Asymmetric()
    asym_deserialized.public_key_deserialization(public_path)
    asym_deserialized.private_key_deserialization(private_path)

    assert asym_deserialized.public_key is not None
    assert asym_deserialized.private_key is not None
    os.remove(public_path)
    os.remove(private_path)


@pytest.mark.parametrize("symmetric_key", [
    os.urandom(16),
    os.urandom(32),
    os.urandom(64)
])
def test_asymmetric_encryption_decryption_parametrized(symmetric_key):
    asym = Asymmetric()
    asym.generate_keys()
    encrypted_key = asym.encrypt(symmetric_key)
    decrypted_key = asym.decrypt(encrypted_key)
    assert decrypted_key == symmetric_key


# Test for Symmetric class
def test_symmetric_key_generation():
    sym = SymmetricCryptography()
    key = sym.generation_key(256)
    assert sym.key is not None
    assert len(key) == 32


def test_symmetric_key_serialization_deserialization():
    sym = SymmetricCryptography()
    key = sym.generation_key(128)
    key_path = "test_symmetric.key"
    sym.key_serialization(key_path)
    sym_deserialized = SymmetricCryptography()
    sym_deserialized.key_deserialization(key_path)
    assert sym_deserialized.key == key
    os.remove(key_path)


@pytest.mark.parametrize("text", [
    "Test message",
    "Test message with numbers 12345",
    "Special characters: !@#$%^&*()",
])
def test_symmetric_encryption_decryption_parametrized(text):
    sym = SymmetricCryptography()
    sym.generation_key(256)
    test_file_path = "test_file.txt"
    encrypted_file_path = "encrypted_file.txt"
    decrypted_file_path = "decrypted_file.txt"
    write_text_to_file(test_file_path, text)
    sym.encrypt(test_file_path, encrypted_file_path)
    decrypted_text = sym.decrypt(encrypted_file_path, decrypted_file_path)
    assert decrypted_text == text
    os.remove(test_file_path)
    os.remove(encrypted_file_path)
    os.remove(decrypted_file_path)


def test_symmetric_encrypt_empty_data():
    sym = SymmetricCryptography()
    sym.generation_key(128)
    test_file_path = "test_file.txt"
    encrypted_file_path = "encrypted_file.txt"
    write_text_to_file(test_file_path, "")
    encrypted = sym.encrypt(test_file_path, encrypted_file_path)
    assert len(encrypted) > 0
    os.remove(test_file_path)
    os.remove(encrypted_file_path)


# Test for file operations
def test_read_json_from_file_success():
    json_data = '{"key": "value"}'
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json_from_file("dummy_path.json")
        assert result == {"key": "value"}


def test_read_json_from_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        result = read_json_from_file("dummy_path.json")
        assert result is None


def test_read_json_from_file_json_decode_error():
    json_data = '{"key": "value"'
    with patch("builtins.open", mock_open(read_data=json_data)):
        result = read_json_from_file("dummy_path.json")
        assert result is None


def test_write_text_to_file_success():
    file_path = "test_file.txt"
    text = "Test text"
    write_text_to_file(file_path, text)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    assert content == text
    os.remove(file_path)


def test_write_text_to_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        write_text_to_file("dummy_path.txt", "Test text")


def test_read_binary_from_file_success():
    file_path = "test_file.bin"
    binary_data = b"Test binary data"
    with open(file_path, 'wb') as file:
        file.write(binary_data)
    result = read_binary_from_file(file_path)
    assert result == binary_data
    os.remove(file_path)


def test_read_binary_from_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        result = read_binary_from_file("dummy_path.bin")
        assert result is None


def test_write_binary_to_file_success():
    file_path = "test_file.bin"
    binary_data = b"Test binary data"
    write_binary_to_file(file_path, binary_data)
    with open(file_path, 'rb') as file:
        content = file.read()
    assert content == binary_data
    os.remove(file_path)


def test_write_binary_to_file_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
        write_binary_to_file("dummy_path.bin", b"Test binary data")
