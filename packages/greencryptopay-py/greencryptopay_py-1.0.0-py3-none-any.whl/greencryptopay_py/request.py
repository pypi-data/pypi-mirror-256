import requests
from .exceptions import GcpSdkRequestException


class Request:
    def __init__(self, api_url: str, testnet: bool):
        testnet = 'testnet/' if testnet else ''
        self.api_url = api_url + testnet
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def set_secret_key(self, secret_key: str):
        if not isinstance(secret_key, str):
            raise TypeError("Invalid argument 'secret_key' must be a string")
        self.headers['X-Secret-Key'] = secret_key

    def get(self, method: str, params: dict, headers: list[dict] = None) -> dict:
        url = self.api_url + method
        if params and len(params) > 0:
            url += '?' + '&'.join([f"{k}={v}" for k, v in params.items()])

        _headers = self.headers.copy()

        if headers and isinstance(headers, dict):
            _headers.update(headers)
        response = requests.get(url, headers=_headers)
        if response.status_code != 200:
            raise GcpSdkRequestException(response.json(), response.status_code)
        return response.json()

    def post(self, method: str, params: dict, headers: list[dict] = None) -> dict:
        _headers = self.headers.copy()
        if headers and isinstance(headers, dict):
            _headers.update(headers)
        response = requests.post(self.api_url + method, headers=_headers, json=params)
        if response.status_code != 200:
            raise GcpSdkRequestException(response.json(), response.status_code)
        return response.json()
