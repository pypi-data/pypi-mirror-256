from datetime import datetime
from typing import Optional

from .utils import add_default_params
from ..request import Request


class Transfer:
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

    def merchant(self, fee_type: str, callback_url: str):
        if not isinstance(fee_type, str):
            raise TypeError("Invalid argument 'fee_type' must be a string")
        if callback_url and not isinstance(callback_url, str):
            raise TypeError("Invalid argument 'callback_url' must be a string")
        return self._request.post('merchant', {"fee_type": fee_type, "callback_url": callback_url})

    def payment_address(self, currency: str,
                        recipient_address: str,
                        fee_type: str,
                        callback_url: str,
                        order_id: str,
                        currency_from: str,
                        amount_from: str) -> dict:

        if not all(isinstance(arg, str) for arg in
                   (currency, recipient_address, fee_type, callback_url, order_id, currency_from, amount_from)):
            raise TypeError("All arguments must be a string")
        return self._request.post('payment_address', {
            "currency": currency, "recipient_address": recipient_address, "fee_type": fee_type,
            "callback_url": callback_url, "merchant_id": self._merchant_id, "order_id": order_id,
            "currency_from": currency_from, "amount_from": amount_from
        })

    def payment_address_state(self, currency: str, payment_address: str) -> dict:
        if not all(isinstance(arg, str) for arg in (currency, payment_address)):
            raise TypeError("Both arguments must be a string")
        return self._request.get('payment_address/state', {"merchant_id": self._merchant_id,
                                                           "currency": currency,
                                                           "payment_address": payment_address})

    def payment_address_payments(self, currency: str,
                                 payment_address: str,
                                 txid: Optional[str] = None,
                                 from_timestamp: Optional[datetime] = None,
                                 to_timestamp: Optional[datetime] = None,
                                 limit: Optional[int] = None,
                                 page: Optional[int] = None,
                                 order: Optional[str] = None) -> dict:

        if not all(isinstance(arg, str) for arg in (currency, payment_address)):
            raise TypeError("Currency and payment_address arguments must be a string")
        params = {"merchant_id": self._merchant_id, "currency": currency, "payment_address": payment_address}
        add_default_params(params,
                           txid=txid,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('payment_address/payments', params)

    def payment_address_callbacks(self, currency: str, payment_address: str,
                                  txid: Optional[str] = None,
                                  from_timestamp: Optional[datetime] = None,
                                  to_timestamp: Optional[datetime] = None,
                                  limit: Optional[int] = None,
                                  page: Optional[int] = None,
                                  order: Optional[str] = None) -> dict:
        if not all(isinstance(arg, str) for arg in (currency, payment_address)):
            raise TypeError("Currency and paymentAddress arguments must be a string")
        params = {"merchant_id": self._merchant_id, "currency": currency, "payment_address": payment_address}
        add_default_params(params,
                           txid=txid,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('payment_address/callbacks', params)

    def merchant_state(self, currency: str) -> dict:
        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        return self._request.get('merchant/state', {"currency": currency, "merchant_id": self._merchant_id})

    def merchant_payment_addresses(self, currency: str,
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

    def merchant_payments(self, currency: str,
                          txid: Optional[str] = None,
                          from_timestamp: Optional[datetime] = None,
                          to_timestamp: Optional[datetime] = None,
                          limit: Optional[int] = None,
                          page: Optional[int] = None,
                          order: Optional[str] = None) -> dict:
        if not isinstance(currency, str):
            raise TypeError("Invalid argument 'currency' must be a string")
        params = {"currency": currency, "merchant_id": self._merchant_id}
        add_default_params(params,
                           txid=txid,
                           from_timestamp=from_timestamp,
                           to_timestamp=to_timestamp,
                           limit=limit,
                           page=page,
                           order=order)
        return self._request.get('merchant/payments', params)
