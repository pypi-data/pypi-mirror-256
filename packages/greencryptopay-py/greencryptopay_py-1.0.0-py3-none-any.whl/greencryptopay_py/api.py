from .Handlers.standard import Standard
from .Handlers.transfer import Transfer
from .request import Request


class Api:
    _STANDARD_URL = 'https://api.greencryptopay.com/standard/v1/'
    _TRANSFER_URL = 'https://api.greencryptopay.com/transfer/v1/'

    @staticmethod
    def standard(testnet: bool = False):
        request = Request(Api._STANDARD_URL, testnet)
        return Standard(request)

    @staticmethod
    def transfer(testnet: bool = False):
        request = Request(Api._TRANSFER_URL, testnet)
        return Transfer(request)
