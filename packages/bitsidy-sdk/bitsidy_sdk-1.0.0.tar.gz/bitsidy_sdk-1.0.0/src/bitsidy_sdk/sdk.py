from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from urllib.parse import quote
from urllib.parse import unquote
import os
import json
import base64
import requests


class BitsidySDK:
    def __init__(self, api_key, store_id):
        self.api_key = api_key
        self.store_id = store_id

    def _pad(self, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()
        return padded_data

    def _unpad(self, padded_data):
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data

    def encrypt_data(self, data):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.api_key.encode()), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padded_data = self._pad(json.dumps(data).encode())
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        iv_and_encrypted_data = base64.b64encode(iv + encrypted).decode('utf-8')
        return quote(iv_and_encrypted_data)

    def decrypt_data(self, data):
        data_buffer = base64.b64decode(unquote(data))
        iv = data_buffer[:16]
        encrypted_text = data_buffer[16:]
        cipher = Cipher(algorithms.AES(self.api_key.encode()), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(encrypted_text) + decryptor.finalize()
        return json.loads(self._unpad(decrypted))

    def create_invoice(self, invoice_data):
        request_data = {
            'storeId': self.store_id,
            'data': self.encrypt_data(invoice_data)
        }

        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post('https://api.bitsidy.com/v1/app/invoice/create', json=request_data, headers=headers)
            response_data = response.json()

            if response_data.get('result') != 'success':
                print(self.decrypt_data(response_data.get('data')).get('message'))
                return False

            return self.decrypt_data(response_data.get('data'))

        except requests.RequestException as e:
            print(f'Error creating invoice: {e}')
            return False

    def get_callback_content(self, encrypted_data):
        return self.decrypt_data(encrypted_data)
