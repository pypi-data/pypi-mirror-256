from decimal import Decimal
from bittrade_kraken_rest.connection.observable import prepare_private
from bittrade_kraken_rest.connection.observable import send
from typing import Callable, TypedDict
from reactivex import compose, operators, Observable
from requests.models import PreparedRequest

from bittrade_kraken_rest.connection.result import send_and_map_to_result

GetWithdrawalInfoResult = TypedDict("GetWithdrawalInfoResult", {"method": str, "limit": str, "amount": str, "fee": str})


def get_withdrawal_info_request(*, asset: str, key: str, amount: Decimal, address: str = "", max_fee: str = ""):
    """
    Get withdrawal info
    :return:
    """
    data = {
        "asset": asset,
        "key": key,
        "amount": str(amount),
    }
    if address:
        data["address"] = address
    if max_fee:
        data["max_fee"] = str(max_fee)
    return prepare_private("/0/private/Withdraw", data=data)


def get_withdrawal_info_result() -> Callable[[Observable[PreparedRequest]], Observable[GetWithdrawalInfoResult]]:
    return send_and_map_to_result(GetWithdrawalInfoResult)
