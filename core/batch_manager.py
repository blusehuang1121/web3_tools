import csv
import time

from web3 import Web3
from enum import Enum

from web3.contract import Contract
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware

from libs.global_config import GlobalConfig


class Network(Enum):
    eth = 1,
    bsc = 2,
    goerli = 3,
    sepolia = 4,
    bsc_test = 5,
    scroll_test_l1 = 6,
    scroll_test_l2 = 7


No_Index = 0
Addr_Index = 1
PriKey_Index = 2


# using https://chainlist.org to find the best RPC url
class BatchManager:
    _web3: Web3
    _contract: Contract
    _current_network: Network
    _nonce_index = 0
    _max_fee_multiply = 1.1
    _last_nonce = -1
    _is_wait_for_complete = False

    _network_info = {
        Network.eth: {
            'rpc': 'https://eth-mainnet.blastapi.io/7612f97c-4943-4f55-872f-e571b941016e',
            'chain_id': 1,
        },
        Network.bsc: {
            'rpc': 'https://rpc.ankr.com/bsc',
            'chain_id': 56,
        },
        Network.goerli: {
            'rpc': 'https://eth-goerli.blastapi.io/7612f97c-4943-4f55-872f-e571b941016e',
            'chain_id': 5,
        },
        Network.sepolia: {
            'rpc': 'https://rpc.sepolia.org',
            'chain_id': 11155111
        },
        Network.bsc_test: {
            'rpc': 'https://bsc-testnet.blastapi.io/7612f97c-4943-4f55-872f-e571b941016e',
            'chain_id': 97
        },
        Network.scroll_test_l1: {
            'rpc': 'https://prealpha.scroll.io/l1',
            'chain_id': 534351
        },
        Network.scroll_test_l2: {
            'rpc': 'https://prealpha.scroll.io/l2',
            'chain_id': 534354
        }
    }

    def __init__(self, network, network_data):
        self._last_nonce = -1

        for net, info in self._network_info.items():
            merged_info = info.copy()
            if not net in network_data.keys():
                continue
            merged_info.update(network_data[net])
            self._network_info[net] = merged_info

        if GlobalConfig().has_rpc_key(network.name):
            self._network_info[Network.eth]['rpc'] = GlobalConfig().get_rpc(network.name)
        network_info = self._network_info[network]

        self._addr = network_info['addr']
        self._chain_id = network_info['chain_id']
        self._rpc = network_info['rpc']
        self._abi = network_info['contract_abi']
        self._current_network = network

        if GlobalConfig().is_use_proxy():
            proxy = GlobalConfig().get_a_proxy()
            self._web3 = Web3(Web3.HTTPProvider(self._rpc, request_kwargs={"proxies": {'https': proxy, 'http': proxy}}))
            print(f"Use proxy {proxy} to make Web3 RPC")
        else:
            self._web3 = Web3(Web3.HTTPProvider(self._rpc))

        self._contract = self._web3.eth.contract(address=self._addr, abi=self._abi)
        self._web3.eth.set_gas_price_strategy(medium_gas_price_strategy)
        self._max_priority_fee_per_gas = self._web3.eth.max_priority_fee
        self._max_fee_per_gas = self._web3.eth.max_priority_fee * 2

        if network in [Network.bsc, Network.bsc_test]:
            self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        elif network in [Network.eth, Network.goerli]:
            self._max_fee_per_gas = self._web3.eth.max_priority_fee + int(
                self._max_fee_multiply * self._web3.eth.get_block('latest')['baseFeePerGas'])

        print(f"Current network: {self._current_network}, Connection status: {self._web3.isConnected()}")

    @staticmethod
    def write_info_to_file(info_data, info_csv_path):
        with open(info_csv_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['No.', 'Address', 'Term', 'Maturity', 'Xen Count'])
            writer.writerows(info_data)

    @staticmethod
    def local_time(timestamp):
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt

    def set_wait_for_complete(self, is_wait):
        self._is_wait_for_complete = is_wait

    def update_mint_gas(self, contract_func, trans_params):
        estimate_param = {
            'chainId': trans_params['chainId'],
            'from': trans_params['from']
        }
        trans_params['gas'] = contract_func.estimate_gas(estimate_param)  # self._web3.toHex(210000)#

        if self._current_network in [Network.bsc, Network.bsc_test]:
            trans_params['gasPrice'] = self._web3.eth.gas_price
        else:
            trans_params['maxFeePerGas'] = self._max_fee_per_gas
            trans_params['maxPriorityFeePerGas'] = self._max_priority_fee_per_gas

    def call_contract_func(self, wallet, func_name, func_args, contract_func, value=0):
        if len(wallet) <= 1:
            return
        addr = wallet[Addr_Index]
        private_key = wallet[PriKey_Index]

        if len(private_key.strip()) <= 0:
            print(f'{addr} private key is empty, ignored.')
            return

        encodedData = self._contract.encodeABI(fn_name=func_name, args=func_args)
        trans_params = {
            'chainId': self._chain_id,
            "from": addr,
            'to': self._addr,
            "nonce": self._web3.eth.getTransactionCount(addr),
            'data': encodedData
        }
        if value > 0:
            trans_params["value"] = value

        self.update_mint_gas(contract_func, trans_params)
        print(f'[Wallet {wallet[No_Index]}] Start to {func_name} from {addr} {trans_params}')
        signed_tx = self._web3.eth.account.signTransaction(trans_params, private_key=private_key)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction sent to chain...{self._web3.toHex(tx_hash)}')
        if self._is_wait_for_complete:
            self._web3.eth.waitForTransactionReceipt(tx_hash)
        # receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)
        # print("Transaction receipt mined: \n")
        # print(dict(receipt))
        # print("Was transaction successful? \n")
        # print(receipt['status'])

    @staticmethod
    def read_wallets_and_callback(csv_path, callback):
        with open(csv_path) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for each_wallet in f_csv:
                callback(each_wallet)

    def is_connect(self):
        return self._web3.isConnected()

    def transfer_money_single(self, amount, from_wallet, to_wallet):
        if len(to_wallet) < 1:
            return
        from_addr = Web3.toChecksumAddress(from_wallet[Addr_Index])
        to_addr = Web3.toChecksumAddress(to_wallet[Addr_Index])
        if from_addr == to_addr:
            return
        nonce = self._web3.eth.get_transaction_count(from_addr)

        while nonce <= self._last_nonce:
            print('.', end=' ')
            time.sleep(1)
            nonce = self._web3.eth.get_transaction_count(from_addr)

        self._last_nonce = nonce
        params = {
            'chainId': self._chain_id,
            'nonce': nonce,
            'from': from_addr,
            'to': to_addr,
            'value': self._web3.toWei(amount, 'ether'),
            'gas': 21000,
        }
        self.update_transfer_gas(from_addr, to_addr, params)
        print(
            f'[wallet {to_wallet[No_Index]}] Transferring {amount} from {from_wallet[Addr_Index]} to {to_wallet[Addr_Index]}, Chain:{self._chain_id}, Nonce:{params["nonce"]}, GasLimit:{params["gas"]}')
        signed_tx = self._web3.eth.account.sign_transaction(params, private_key=from_wallet[PriKey_Index])
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Eth Transfer sent to chain...{self._web3.toHex(tx_hash)}')
        if self._is_wait_for_complete:
            self._web3.eth.waitForTransactionReceipt(tx_hash)
        # print("Transaction receipt mined: \n")

    def transfer_money(self, amount, from_wallet, csv_path):
        to_wallets = []
        callback = lambda wallet: {
            to_wallets.append(wallet)
        }
        self.read_wallets_and_callback(csv_path, callback)

        for to_wallet in to_wallets:
            self.transfer_money_single(amount, from_wallet, to_wallet)

    def update_transfer_gas(self, from_addr, to_addr, trans_params):
        estimate_gas = self._web3.eth.estimateGas({'to': from_addr, 'from': to_addr, 'value': 0})
        trans_params['gas'] = estimate_gas

        if self._current_network in [Network.eth, Network.goerli]:
            trans_params['maxFeePerGas'] = max(self._max_fee_per_gas, self._web3.toWei(3, 'gwei'))
            trans_params['maxPriorityFeePerGas'] = max(self._max_priority_fee_per_gas, self._web3.toWei(1.5, 'gwei'))
        else:
            trans_params['gasPrice'] = self._web3.eth.gas_price

    def get_balance(self, wallet):
        return self._web3.fromWei(self._web3.eth.getBalance(Web3.toChecksumAddress(wallet[Addr_Index])), "ether")

    def batch_get_balance(self, csv_path):
        wallets = []
        callback = lambda wallet: {
            wallets.append(wallet)
        }
        self.read_wallets_and_callback(csv_path, callback)
        for wallet in wallets:
            if len(wallet) < 1:
                continue
            balance = self._web3.fromWei(self._web3.eth.getBalance(Web3.toChecksumAddress(wallet[Addr_Index])), "ether")
            print(f'Wallet {wallet[No_Index]} {wallet[Addr_Index]} balance {balance}')
