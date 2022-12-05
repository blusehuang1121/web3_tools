from web3 import Web3

from core.batch_manager import Network, Addr_Index
from core.batch_mint_manager import BatchMintManager
from libs.common import get_file_path


class ToolHelper:
    _erc721_abi: str = '[{"inputs":[{"internalType":"string","name":"name_","type":"string"},{"internalType":"string","name":"symbol_","type":"string"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
    _network: Network = Network.eth
    _addr = ''
    _abi = '[]'
    _gas_limit = 21000
    _gas_max_fee = 1
    _gas_priority_fee = 1.5
    _is_gas_limit = False
    _value = 0
    _is_wait_for_complete = False

    def contract(self, addr):
        return ContractRunner(Web3.toChecksumAddress(addr))

    def network(self, network):
        self._network = network
        return self

    def abi(self, c_abi):
        self._abi = c_abi
        return self

    def gas_limit(self, limit):
        self._is_gas_limit = True
        self._gas_limit = limit
        return self

    def gas_max_fee(self, price):
        self._gas_max_fee = price
        return self

    def gas_priority_fee(self, p_fee):
        self._gas_priority_fee = p_fee
        return self

    def get_balance(self, wallet):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        return b.get_balance(wallet)

    def value(self, amount=0):
        self._value = Web3.toWei(amount, 'ether')
        return self

    def transfer_eth(self, amount, from_wallet, to_wallets_csv):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        b.transfer_money(amount, from_wallet, to_wallets_csv)

    def transfer_eth_single(self, amount, from_wallet, to_wallet):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        b.set_wait_for_complete(self._is_wait_for_complete)
        b.transfer_money_single(amount, from_wallet, to_wallet)


class ContractRunner(ToolHelper):
    def __init__(self, addr):
        self._addr = addr
        self._abi = self._erc721_abi
        self._is_transfer = False
        self._transfer_to_addr = ''
        self._wallet_file_path = ''
        self._wallet = []
        self._is_single_wallet = False

    def only_scan(self):
        self._is_transfer = False
        self._transfer_to_addr = ''
        return self

    def transfer_to(self, to_addr):
        self._is_transfer = True
        self._transfer_to_addr = to_addr
        return self

    def wallets(self, wallet_file_path):
        self._wallet_file_path = get_file_path(wallet_file_path)
        self._is_single_wallet = False
        return self

    def wallet(self, wallet):
        self._wallet = wallet
        self._is_single_wallet = True
        return self

    def collect_nft(self):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        b.batch_collect_nft(self._wallet_file_path, self._transfer_to_addr, self._is_transfer)

    def call_read(self, method_name, args):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        return b.call_read_func_with_args(method_name, args)

    def wait_for_complete(self, is_wait):
        self._is_wait_for_complete = is_wait
        return self

    def call_write(self, method_name, args):
        network_data = {
            self._network: {
                'addr': self._addr,
                'contract_abi': self._abi
            }
        }
        b = BatchMintManager(self._network, network_data)
        b.set_wait_for_complete(self._is_wait_for_complete)
        if self._is_gas_limit:
            b.limit_gas(self._gas_limit, self._gas_max_fee, self._gas_priority_fee)

        if self._is_single_wallet:
            if self._value > 0:
                b.single_call_write_func_with_value(self._wallet, self._value, method_name, args)
            else:
                b.single_call_write_func(self._wallet, method_name, args)
        else:
            if self._value > 0:
                b.batch_call_write_func_with_value(self._wallet_file_path, self._value, method_name, args)
            else:
                b.batch_call_write_func(self._wallet_file_path, method_name, args)
