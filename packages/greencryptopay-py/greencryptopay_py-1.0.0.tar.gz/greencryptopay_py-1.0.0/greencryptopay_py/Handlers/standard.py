from datetime import datetime
from typing import Optional

from .utils import add_default_params
from ..request import Request


class Standard:
    def __init__(self, request: Request):
        if not isinstance(request, Request):
            raise TypeError("The 'request' argument must be an instance of Request")
        self._request = request
        self._merchant_id = None

    def set_merchant_id(self, merchant_id: str):
        if not isinstance(merchant_id, str):
            raise TypeError("Invalid argument 'merchant_id' must be a string")
        self._merchant_id = merchant_id

    def set_secret_key(self, secret_key: str):
        self._request.set_secret_key(secret_key)

    def merchant(self, fee_type: str, callback_url: Optional[str] = None):
        if not isinstance(fee_type, str):
            raise TypeError("Invalid argument 'fee_type' must be a string")
        if callback_url and not isinstance(callback_url, str):
            raise TypeError("Invalid argument 'callback_url' must be a string")
        return self._request.post('merchant', {"fee_type": fee_type, "callback_url": callback_url})

    def payment_address(self, currency: str,
                        callback_url: str,
                        order_id: str,
                        currency_from: str,
                        amount_from: str) -> dict:
        if not all(isinstance(arg, str) for arg in [currency, callback_url, order_id, currency_from, amount_from]):
            raise TypeError("All arguments must be strings")
        return self._request.post('payment_address', {
            "merchant_id": self._merchant_id,
            "currency": currency,
            "callback_url": callback_url,
            "order_id": order_id,
            "currency_from": currency_from,
            "amount_from": amount_from
        })

    def withdraw(self, currency: str, recipients: list[dict]) -> dict:
        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        if not all(isinstance(recipient, dict) for recipient in recipients):
            raise TypeError("Invalid argument 'recipients' must be a list of dictionaries")
        return self._request.post('withdraw',
                                  {"merchant_id": self._merchant_id, "currency": currency, "recipients": recipients})

    def withdraw_all(self, currency: str, recipient_address: str) -> dict:
        if not isinstance(currency, str) or not isinstance(recipient_address, str):
            raise TypeError("Invalid arguments. currency and recipient_address must be strings")
        return self._request.post('withdraw_all', {"merchant_id": self._merchant_id, "currency": currency,
                                                   "recipient_address": recipient_address})

    def merchant_state(self, currency: str) -> dict:
        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        return self._request.get('merchant/state', {"merchant_id": self._merchant_id, "currency": currency})

    def merchant_payment_address(self, currency: str,
                                 from_timestamp: Optional[datetime] = None,
                                 to_timestamp: Optional[datetime] = None,
                                 limit: Optional[int] = None,
                                 page: Optional[int] = None,
                                 order: Optional[str] = None) -> dict:

        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        params = {"currency": currency, "merchant_id": self._merchant_id}
        add_default_params(params,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('merchant/payment_addresses', params)

    def merchant_incoming_payments(self, currency: str,
                                   payment_address: Optional[str] = None,
                                   txid: Optional[str] = None,
                                   from_timestamp: Optional[datetime] = None,
                                   to_timestamp: Optional[datetime] = None,
                                   limit: Optional[int] = None,
                                   page: Optional[int] = None,
                                   order: Optional[str] = None) -> dict:

        if not isinstance(currency, str):
            raise TypeError("Invalid argument. Currency must be string")
        if payment_address and not isinstance(payment_address, str):
            raise TypeError("Invalid argument. Payment_address must be string")
        params = {"currency": currency, "merchant_id": self._merchant_id}
        if payment_address is not None:
            params['payment_address'] = payment_address
        add_default_params(params,
                           txid=txid,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('merchant/incoming_payments', params)

    def merchant_withdrawals(self, currency: str,
                             from_timestamp: Optional[datetime] = None,
                             to_timestamp: Optional[datetime] = None,
                             limit: Optional[int] = None,
                             page: Optional[int] = None,
                             order: Optional[str] = None) -> dict:

        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        params = {"currency": currency, "merchant_id": self._merchant_id}
        add_default_params(params,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('merchant/withdrawals', params)

    def payment_address_callbacks(self, currency: str,
                                  payment_address: str,
                                  txid: Optional[str] = None,
                                  from_timestamp: Optional[datetime] = None,
                                  to_timestamp: Optional[datetime] = None,
                                  limit: Optional[int] = None,
                                  page: Optional[int] = None,
                                  order: Optional[str] = None) -> dict:

        if not isinstance(currency, str) or not isinstance(payment_address, str):
            raise TypeError("Invalid arguments. currency and payment_address must be strings")
        params = {"currency": currency, "merchant_id": self._merchant_id, "payment_address": payment_address}
        add_default_params(params,
                           txid=txid,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('payment_address/callbacks', params)

    def payment_address_state(self, currency: str, payment_address: str) -> dict:
        if not isinstance(currency, str) or not isinstance(payment_address, str):
            raise TypeError("Invalid arguments. currency and payment_address must be strings")
        return self._request.get('payment_address/state', {"merchant_id": self._merchant_id, "currency": currency,
                                                           "payment_address": payment_address})
