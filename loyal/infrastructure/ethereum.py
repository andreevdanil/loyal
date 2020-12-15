import json
from pathlib import Path
from typing import Dict, TypedDict

import attr
from web3 import Web3, WebsocketProvider
from web3.contract import ContractFunctions

__all__ = (
    "EthConfig",
    "EthereumService",
    "make_eth_client",
)

CURRENT_DIR = Path(__file__).parent


class EthConfig(TypedDict):
    node_url: str
    contract_address: str


@attr.s(auto_attribs=True, slots=True, frozen=True)
class EthereumService:
    functions: ContractFunctions

    def get_balance(self, account_address: str) -> float:
        adr = Web3.toChecksumAddress(account_address)
        balance = self.functions.getBalance(adr).call()
        return balance


def make_eth_client(config: EthConfig) -> EthereumService:
    provider = WebsocketProvider(config["node_url"])
    w3 = Web3(provider)

    contract_path = CURRENT_DIR / "loyal.json"
    contract = json.loads(contract_path.read_bytes())
    contract = w3.eth.contract(config["contract_address"], abi=contract["abi"])

    return EthereumService(contract.functions)
