from pathlib import Path
from typing import Dict, TypedDict

import attr
from solcx import compile_source
from web3 import Web3, WebsocketProvider
from web3.contract import ContractFunctions

__all__ = (
    "EthConfig",
    "EthereumService",
    "make_eth_client",
)

CURRENT_DIR = Path(__file__).parent


def compile_abi(contract_path: Path) -> Dict:
    contract = contract_path.read_text()
    compiled_file = compile_source(contract, output_values=["abi"]).popitem()
    return compiled_file[1]["abi"]


class EthConfig(TypedDict):
    node_url: str
    contract_address: str


@attr.s(auto_attribs=True, slots=True, frozen=True)
class EthereumService:
    functions: ContractFunctions

    def get_balance(self, account_address: str) -> float:
        balance = self.functions.getBalance(account_address).call()
        return balance


def make_eth_client(config: EthConfig) -> EthereumService:
    provider = WebsocketProvider(config["node_url"])
    w3 = Web3(provider)

    contract_path = CURRENT_DIR / "contract.sol"
    abi = compile_abi(contract_path)
    contract = w3.eth.contract(config["contract_address"], abi=abi)

    return EthereumService(contract.functions)