# Greencryptopay library for Python

The Greencryptopay library for Python allows you to easily integrate the Greencryptopay payment system into your Python projects. This library provides convenient methods for interacting with the Greencryptopay API.

## Installation

You can install this package using pip:

```sh
pip install greencryptopay-py
```

## Dependencies 
This package depends on the "requests" library version ^2.31.0. If it's not already installed, it will be automatically installed when you install this library.

## Standard API
- [Standard API](https://greencryptopay.com/ru/standard)

> **Getting Started:**

```python
from greencryptopay_py import Api

# Standard API
standard_api = Api.standard()

# Standard API testnet
standard_api = Api.standard(True)

# Sign up
if not merchant_id or not secret_key:
    data = standard_api.merchant('percent', 'https://example.com/callback')
    merchant_id = data['merchant_id']
    secret_key = data['secret_key']

standard_api.set_merchant_id(merchant_id)
standard_api.set_secret_key(secret_key)

```

> **Sign up:**

| Name    | Parameters                                              | Validation | Description |
| :----  |:--------------------------------------------------------|  :----  |:---- |
| merchant | <ul><li>str fee_type</li><li>str callback_url</li></ul> | <ul><li>Enum: [percent, fix]</li><li>Max: 200</li></ul> | <ul><li>Fee type</li><li>URL to send notifications about payments</li></ul>  |


> **Operations:**

| Name    | Parameters                                                                                                                     | Validation | Description |
| :----  |:-------------------------------------------------------------------------------------------------------------------------------|  :----  |:---- |
| payment_address | <ul><li>str currency</li><li>str callback_url</li> <li>str orderId</li> <li>str currencyFrom</li> <li>str amountFrom</li></ul> | <ul><li>Enum: [btc]</li><li>Max: 200</li> <li>Max: 50</li> <li>Enum: [usd]</li> <li> — </li></ul> | <ul><li>Currency</li><li>URL to send notifications about payments</li> <li>Order identifier in your system</li> <li>Currency to convert from</li> <li>Amount to convert</li></ul> |
| withdraw | <ul><li> str currency </li><li> array recipients </li></ul>                                                                    | <ul><li> Enum: [btc] </li><li> — </li></ul> | <ul><li> Currency </li><li>Array structure:  [['address' => 'Recipient address', 'amount' => 'Recipient's amount']] </li></ul>  |
| withdraw_all | <ul><li> str currency </li><li> str recipientAddress </li></ul>                                                                | <ul><li> Enum: [btc] </li><li> — </li></ul> | <ul><li> Currency </li><li> Recipient address </li></ul>  |

> **Stats:**

| Name    | Parameters                                                                                                                                                                                                                                            | Validation | Description |
| :----  |:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|  :----  |:---- |
| merchant_state | <ul><li> str currency </li></ul>                                                                                                                                                                                                                      | <ul><li> Enum: [btc] </li></ul> | <ul><li> Currency </li></ul>  |
| merchant_payment_address | <ul><li> str currency </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int / none limit </li><li> int / none page </li><li>str / none order</li></ul>                                                                  | <ul><li> Enum: [btc] </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li>Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Address creation timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59")</li><li>Address creation timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| merchant_incoming_payments | <ul><li> str currency </li><li> str / none payment_address </li><li> str / none txid </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int / none limit </li><li> int / none page </li><li> str / none order </li></ul> | <ul><li> Enum: [btc] </li><li> — </li><li> — </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Show only payments to specific payment address </li><li> Show only payments with specific transaction </li><li> Payment timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Payment timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| merchant_withdrawals | <ul><li> str currency </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int / none limit </li><li> int / none page </li><li> str / none order </li></ul>                                                                | <ul><li>Enum: [btc] </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency</li><li>Withdrawal timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Withdrawal timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| payment_address_callbacks  | <ul><li> str currency </li><li> str payment_address </li><li> str / none txid </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int  / none limit </li><li> int  / none page </li><li> str / none order </li></ul>      | <ul><li>Enum: [btc] </li><li> — </li><li> — </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Payment address </li><li> Show only payment callbacks with specific transaction </li><li> Callback timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Callback timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| payment_address_state | <ul><li> str currency </li><li> str payment_address </li></ul>                                                                                                                                                                                        | <ul><li> Enum: [btc] </li><li> — </li></ul> | <ul><li> Currency </li><li> Payment address </li></ul>  |

## Transfer API

- [Transfer API](https://greencryptopay.com/ru/transfer)

> **Getting Started:**

```python
from greencryptopay_py import Api

# Transfer API
transfer_api = Api.transfer()

# Transfer API testnet
transfer_api = Api.transfer(True)

# Sign up
if not merchant_id or not secret_key:
    data = transfer_api.merchant('percent', 'https://example.com/callback')
    merchant_id = data['merchant_id']
    secret_key = data['secret_key']

transfer_api.set_merchant_id(merchant_id)
transfer_api.set_secret_key(secret_key)

```

> **Sign up:**

| Name    | Parameters                                              | Validation | Description |
| :----  |:--------------------------------------------------------|  :----  |:---- |
| merchant | <ul><li>str fee_type</li><li>str callback_url</li></ul> | <ul><li>Enum: [percent, fix]</li><li>Max: 200</li></ul> | <ul><li>Fee type</li><li>URL to send notifications about payments</li></ul>  |

> **Operations:**

| Name            | Parameters                                                                                                                                                                                  | Validation | Description |
|:----------------|:--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|  :----  |:---- |
| payment_address | <ul><li> str currency </li><li> str recipientAddress </li><li> str fee_type </li><li> str callback_url </li><li> str orderId </li><li> str currencyFrom </li><li> str amountFrom </li></ul> | <ul><li>Enum: [btc] </li><li> — </li><li>Enum: [percent, fix] </li><li> Max:200 </li><li> Max:50 </li><li> Enum: [usd, rub, try, eur, zar, gbp, uah, aud, brl, pln] </li><li> — </li></ul> | <ul><li> Currency </li><li> Recipient address </li><li> Fee type </li><li> URL to send notifications about payments </li><li> Order identifier in your system </li><li> Currency to convert from </li><li> Amount to convert </li></ul>  |

> **Stats:**

| Name                      | Parameters                                                                                                                                                                                                                                       | Validation | Description |
|:--------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|  :----  |:---- |
| payment_address_state     | <ul><li> str currency </li><li> str payment_address </li></ul>                                                                                                                                                                                   | <ul><li> Enum: [btc] </li><li> — </li></ul> | <ul><li> Currency </li><li> Show only payments to specific payment address </li></ul>  |
| payment_address_payments  | <ul><li> str currency </li><li> str payment_address </li><li> str / none txid </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int  / none limit </li><li> int  / none page </li><li> str / none order </li></ul> | <ul><li> Enum: [btc]  </li><li> — </li><li> — </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Payment address </li><li> Show only specific transaction payments </li><li> Payment timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Payment timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| payment_address_callbacks | <ul><li> str currency </li><li> str payment_address </li><li> str / none txid </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int  / none limit </li><li> int  / none page </li><li> str / none order </li></ul> | <ul><li>Enum: [btc] </li><li> — </li><li> — </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Payment address </li><li> Show only payment callbacks with specific transaction </li><li> Payment timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Payment timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| merchant_state            | <ul><li> str currency </li></ul>                                                                                                                                                                                                                 | <ul><li> Enum: [btc] </li></ul> | <ul><li> Currency </li></ul>  |
| merchant_payment_address  | <ul><li> str currency </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int / none limit </li><li> int / none page </li><li>str / none order</li></ul>                                                             | <ul><li> Enum: [btc] </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li>Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Address creation timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59")</li><li>Address creation timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59") </li><li> Number of records in the response </li><li> Page number </li><li> Records order ascending or descending </li></ul>  |
| merchant_payments         | <ul><li> str currency </li><li> str / none txid  </li><li> str / none from_timestamp </li><li> str / none to_timestamp </li><li> int  / none limit </li><li> int  / none page </li><li> str / none order </li></ul>                              | <ul><li> Enum: [btc] </li><li> — </li><li> Timestamp in UTC </li><li> Timestamp in UTC </li><li> Min:1, Max:200 </li><li> Min:1 </li><li> Enum: [asc, desc] </li></ul> | <ul><li> Currency </li><li> Show only specific transaction payments </li><li> Payment timestamp in UTC, from (inclusive, ex. "2035-12-31T15:30:59") </li><li> Payment timestamp in UTC, to (inclusive, ex. "2035-12-31T15:30:59")  </li><li> Number of records in the response  </li><li> Page number  </li><li> Records order ascending or descending </li></ul>  |

