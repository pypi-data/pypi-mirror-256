import asyncio
import logging
from typing import Optional, Tuple

import a_sync
from multicall import Call

from y import ENVIRONMENT_VARIABLES as ENVS
from y import convert
from y.classes.common import ERC20, WeiBalance
from y.contracts import has_methods
from y.datatypes import AnyAddressType, Block, UsdPrice, UsdValue
from y.exceptions import call_reverted
from y.utils import gather_methods

_RESERVES_METHODS = 'token0()(address)', 'token1()(address)', 'usersAmounts()((uint,uint))'

logger = logging.getLogger(__name__)


@a_sync.a_sync(default='sync', cache_type='memory')
async def is_popsicle_lp(token_address: AnyAddressType) -> bool:
    # NOTE: contract to check for reference (mainnet): 0xd2C5A739ebfE3E00CFa88A51749d367d7c496CCf
    return await has_methods(token_address, ('token0()(address)','token1()(address)','usersAmounts()((uint,uint))'), sync=False)

@a_sync.a_sync(default='sync')
async def get_price(token: AnyAddressType, block: Optional[Block] = None, *, skip_cache: bool = ENVS.SKIP_CACHE) -> Optional[UsdPrice]:
    address = convert.to_address(token)
    total_val = await get_tvl(address, block, skip_cache=skip_cache, sync=False)
    if total_val is None:
        return None
    total_supply = await ERC20(address, asynchronous=True).total_supply_readable(block, sync=False)
    return UsdPrice(total_val / total_supply)

@a_sync.a_sync(default='sync')
async def get_tvl(token: AnyAddressType, block: Optional[Block] = None, skip_cache: bool = ENVS.SKIP_CACHE) -> Optional[UsdValue]:
    balances: Tuple[WeiBalance, WeiBalance]
    balances = await get_balances(token, block, skip_cache=skip_cache, _async_balance_objects=True, sync=False)
    if balances is None:
        return None
    return UsdValue(sum(await asyncio.gather(*[bal.value_usd for bal in balances])))

@a_sync.a_sync(default='sync')
async def get_balances(token: AnyAddressType, block: Optional[Block] = None, skip_cache: bool = ENVS.SKIP_CACHE, _async_balance_objects: bool = False) -> Optional[Tuple[WeiBalance,WeiBalance]]:
    try:
        token0, token1, (balance0, balance1) = await gather_methods(convert.to_address(token), _RESERVES_METHODS, block=block)
    except Exception as e:
        if call_reverted(e):
            return None
        elif str(e) == "not enough values to unpack (expected 3, got 2)":
            # TODO determine if this is regular behavior when no tvl in pool or if this is bug to fix
            return None
        raise
    balance0 = WeiBalance(balance0, token0, block=block, skip_cache=skip_cache, asynchronous=_async_balance_objects)
    balance1 = WeiBalance(balance1, token1, block=block, skip_cache=skip_cache, asynchronous=_async_balance_objects)
    return balance0, balance1
