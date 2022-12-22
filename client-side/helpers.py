import requests
import json
import hashlib
from Crypto.Cipher import AES

base_url = 'http://localhost:8000'

def creds(username:str, password: str):
    return json.dumps({
        "username": username,
        "password": password
    })

def request_data(username:str, password: str):
    url = f"{base_url}/retrieve_data"
    response = requests.post(url=url, data=creds(username, password))
    res = response.json()
    if not res['data']:
        return ""
    key = make_key(username, password)
    decrypted = decrypt_data(bytes.fromhex(res['nonce']), key, bytes.fromhex((res['data'])))
    return json.loads(decrypted)

def register(username:str, password: str):
    url = f"{base_url}/register"
    response = requests.post(url=url, data=creds(username, password))
    return response.json()

def update_creds(username:str, password: str, url:str, url_uname: str, url_password: str):
    """ retrieves encrypted data from server, decrypts, modifies and sends request to server for the update"""
    data = request_data(username, password)
    if data:
        data[url]= {url_uname: url_password}
    else:
        data = {url: {url_uname: url_password}}
    return update_data(username, password, data)

def update_data(username:str, password: str, data: dict):
    """ encrypts data and send request to server for update"""
    url = f"{base_url}/update"
    payload = {
        "username": username,
        "password": password
    }
    key = make_key(username, password)
    nonce, enc_data = encrypt_data(key, json.dumps(data))
    payload['nonce'] = nonce.hex()
    payload['data'] = enc_data.hex()
    response = requests.put(url=url, data=json.dumps(payload))
    return response.json()

def make_key(username: str, password: str):
    """ generates key for encryption out of username and password"""
    m = hashlib.sha256()
    m.update(username.encode())
    salt = m.digest()[:32]
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 10000)
    return key

def encrypt_data(key: bytes, data: dict):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return nonce, ciphertext

def decrypt_data(nonce: bytes, key: bytes, encrypted_data: bytes):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(encrypted_data)
