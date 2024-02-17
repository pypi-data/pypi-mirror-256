import base64
from tonsdk.provider import ToncenterClient, prepare_address, address_state

import asyncio
from tonsdk.boc import begin_cell, Cell
import aiohttp
import json
from typing import Dict

from tonsdk.utils import Address
from tonpy import CellSlice

__all__ = ["TonCenterClient", "ToncenterWrongResult"]


class ToncenterWrongResult(Exception):
    def __init__(self, code):
        self.code = code


class TonCenterClient:
    def __init__(self, api_key: str, testnet: bool = True):
        base_url = f"https://{'testnet.' if testnet else ''}toncenter.com/api/v2/"
        self.provider = ToncenterClient(base_url=base_url, api_key=api_key)

    async def run_get_method(self, addr: str, method: str, stack: list):
        addr = prepare_address(addr)
        result = await self._run(self.provider.raw_run_method(addr, method, stack))

        if result.get("@type") == "smc.runResult" and "stack" in result:
            result = result["stack"]

        return result[0][1]

    async def get_oracle_data(self, addr: str, method: str, stack: list):
        addr = prepare_address(addr)
        result = await self._run(self.provider.raw_run_method(addr, method, stack))
        if result.get("@type") == "smc.runResult" and "stack" in result:
            result = result["stack"]

        return result

    async def get_estimate(self, addr: str, method: str, stack: list):
        addr = prepare_address(addr)
        result = await self._run(self.provider.raw_run_method(addr, method, stack))
        if result.get("@type") == "smc.runResult" and "stack" in result:
            result = result["stack"]
        return result

    async def get_transactions(self, params):
        req = {
            "func": self.__jsonrpc_request,
            "args": ["getTransactions"],
            "kwargs": {"params": params},
        }
        result = await self._run(req)
        return result

    async def get_address_state(self, address):
        req = {
            "func": self.__jsonrpc_request,
            "args": ["getAddressState"],
            "kwargs": {"params": {"address": address}},
        }
        result = await self._run(req)

        return result

    async def get_address_balance(self, address):
        req = {
            "func": self.__jsonrpc_request,
            "args": ["getAddressBalance"],
            "kwargs": {"params": {"address": address}},
        }
        result = await self._run(req)

        return result

    async def get_jetton_metadata(self, jetton_address):
        req = {
            "func": self.__jsonrpc_request,
            "args": ["getTokenData"],
            "kwargs": {"params": {"address": jetton_address}},
        }
        result = await self._run(req)
        return result

    async def get_jetton_wallet(self, master_address, account_address):
        request_stack = [
            [
                "tvm.Slice",
                base64.b64encode(
                    begin_cell().store_address(account_address).end_cell().to_boc()
                ).decode(),
            ]
        ]
        # get jetton wallet address from master address
        stack = await self.run_get_method(
            addr=master_address.to_string(),
            method="get_wallet_address",
            stack=request_stack,
        )
        jetton_wallet_address = (
            Cell.one_from_boc(base64.b64decode(stack["bytes"]))
            .begin_parse()
            .read_msg_addr()
            .to_string(True, True, True)
        )
        return jetton_wallet_address

    async def get_token_balance(self, master_address, account_address):
        jetton_wallet_address = await self.get_jetton_wallet(
            master_address, account_address
        )
        # get token balance from jetton wallet address
        req = {
            "func": self.__jsonrpc_request,
            "args": ["getTokenData"],
            "kwargs": {"params": {"address": jetton_wallet_address}},
        }
        result = await self._run(req)
        return result["balance"]

    async def get_address_information(self, address):
        address = prepare_address(address)
        result = await self._run(self.provider.raw_get_account_state(address))

        result["state"] = address_state(result)

        return result["state"]

    async def get_alarm_address(self, oracle, alarm_id):
        result = await self.run_get_method(
            oracle, "getAlarmAddress", [["num", alarm_id]]
        )
        address_bytes = result["bytes"]
        cs = CellSlice(address_bytes)
        address = cs.load_address()
        return address

    async def get_alarm_info(self, alarm_address: str):
        alarm_addr = prepare_address(alarm_address)
        result = await self._run(
            self.provider.raw_run_method(alarm_addr, "getAlarmMetadata", [])
        )

        if result.get("@type") == "smc.runResult" and "stack" in result:
            result = result["stack"]

        watchmaker_address = CellSlice(result[0][1]["bytes"]).load_address()
        base_asset_scale = int(result[1][1], 16)
        quote_asset_scale = int(result[2][1], 16)
        remain_scale = int(result[3][1], 16)
        base_asset_price = 1000 * (int(result[4][1], 16) / 2**64)
        base_asset_amount = int(result[5][1], 16) / 10**9
        quote_asset_amount = int(result[6][1], 16) / 10**6
        created_at = int(result[7][1], 16)

        return {
            "watchmaker_address": watchmaker_address,
            "base_asset_scale": base_asset_scale,
            "quote_asset_scale": quote_asset_scale,
            "remain_scale": remain_scale,
            "base_asset_price": base_asset_price,
            "base_asset_amount": base_asset_amount,
            "quote_asset_amount": quote_asset_amount,
            "created_at": created_at,
        }

    async def send_boc(self, boc):
        return await self._run(self.provider.raw_send_message(boc))

    async def _run(self, to_run):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            func = to_run["func"]
            args = to_run["args"]
            kwargs = to_run["kwargs"]
            return await func(session, *args, **kwargs)

    async def __post_request(self, session, url, data):
        async with session.post(
            url, data=json.dumps(data), headers=self.__headers()
        ) as resp:
            return await self.__parse_response(resp)

    async def __jsonrpc_request(
        self, session, method: str, params: Dict, id: str = "1", jsonrpc: str = "2.0"
    ):
        payload = {
            "id": id,
            "jsonrpc": jsonrpc,
            "method": method,
            "params": params,
        }

        async with session.post(
            self.provider.base_url + "jsonRPC", json=payload, headers=self.__headers()
        ) as resp:
            return await self.__parse_response(resp)

    def __headers(self):
        headers = {
            "Content-Type": "application/json",
            "accept": "application/json",
        }
        if self.provider.api_key:
            headers["X-API-Key"] = self.provider.api_key

        return headers

    async def __parse_response(self, resp):
        try:
            resp = await resp.json()
        except Exception:  # TODO: catch correct exceptions
            raise ToncenterWrongResult(resp.status)

        if not resp["ok"]:
            raise ToncenterWrongResult(resp["code"])

        return resp["result"]
