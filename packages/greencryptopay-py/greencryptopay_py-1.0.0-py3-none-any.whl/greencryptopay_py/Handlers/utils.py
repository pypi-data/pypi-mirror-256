from datetime import datetime
from typing import Optional


def add_default_params(
        params: dict,
        txid: Optional[str] = None,
        from_timestamp: Optional[datetime] = None,
        to_timestamp: Optional[datetime] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        order: Optional[str] = None):
    if txid:
        params['txid'] = txid
    if from_timestamp:
        params['from_timestamp'] = from_timestamp
    if to_timestamp:
        params['to_timestamp'] = to_timestamp
    if limit:
        params['limit'] = limit
    if page:
        params['page'] = page
    if order:
        params['order'] = order
