from helpers import *


def test_encryption():
    """ test encryption"""
    username = 'test'
    password = 'test'
    data_to_encrypt = {"url": {"name": "pass"}}
    key = make_key(username, password)
    nonce, enc_data = encrypt_data(key, json.dumps(data_to_encrypt))
    dec = decrypt_data(nonce, key, enc_data)
    assert data_to_encrypt == dec