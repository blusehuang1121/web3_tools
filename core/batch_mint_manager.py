import json

import requests
from web3 import Web3
from core.batch_manager import BatchManager, Network, Addr_Index, No_Index
from libs.common import REPLACE_WALLET_ADDR
from libs.global_config import GlobalConfig


class BatchMintManager(BatchManager):
    _is_gas_limited = False
    _gas_max_fee = 10
    _gas_limit = 200000
    _priority_fee = 1.5

    def __init__(self, network: Network = Network.eth, network_data: dict = {}) -> None:
        super().__init__(network, network_data)
        self.moralis_key = GlobalConfig().moralis_key()

    def limit_gas(self, gas_limit, max_fee, priority_fee=1.5):
        self._is_gas_limited = True
        self._gas_max_fee = max_fee
        self._gas_limit = gas_limit
        self._priority_fee = priority_fee

    def call_read_func_with_args(self, func_name, func_args: tuple):
        result = self._contract.get_function_by_name(func_name)(*func_args).call()
        print(result)
        return result

    def call_read_func(self, func_name):
        result = self._contract.get_function_by_name(func_name)().call()
        print(result)
        return result

    def batch_call_write_func_with_value(self, csv_path, value, func_name, func_args):
        callback = lambda wallet: {
            self.each_call_func(wallet, value, func_name, func_args)
        }
        self.read_wallets_and_callback(csv_path, callback)

    def batch_call_write_func(self, csv_path, func_name, func_args):
        callback = lambda wallet: {
            self.each_call_func(wallet, 0, func_name, func_args)
        }
        self.read_wallets_and_callback(csv_path, callback)

    def each_call_func(self, wallet, value, func_name, func_args: tuple):
        func_name = func_name
        args = []

        if type(func_args) == tuple:
            arg_list = list(func_args)
            for index, arg in enumerate(arg_list):
                if arg_list[index] == REPLACE_WALLET_ADDR:
                    arg_list[index] = wallet[Addr_Index]
            func_args = tuple(arg_list)

            contract_func = self._contract.get_function_by_name(func_name)(*func_args)
            for arg in func_args:
                args.append(arg)
        else:
            contract_func = self._contract.get_function_by_name(func_name)(func_args)
            args.append(func_args)
        try:
            self.call_contract_func(wallet, func_name, args, contract_func, value)
        except Exception as e:
            print(f'Call contract func has an error {wallet[Addr_Index]}, {repr(e)}')

    def update_mint_gas(self, contract_func, trans_params):
        if not self._is_gas_limited:
            super().update_mint_gas(contract_func, trans_params)
        else:
            trans_params['gas'] = self._gas_limit
            if self._current_network in [Network.bsc, Network.bsc_test]:
                trans_params['gasPrice'] = self._web3.eth.gas_price
            else:
                trans_params['maxFeePerGas'] = self._web3.toWei(self._gas_max_fee, 'gwei')
                trans_params['maxPriorityFeePerGas'] = self._web3.toWei(self._priority_fee, 'gwei')

    def batch_collect_nft(self, csv_path, to_addr, is_transfer):
        callback = lambda wallet: {
            self.each_collect_nft(wallet, to_addr, is_transfer)
        }
        self.read_wallets_and_callback(csv_path, callback)

    def each_collect_nft(self, wallet, to_addr, is_transfer):
        headers = {
            "accept": "application/json",
            "X-API-Key": self.moralis_key
        }

        url = f"https://deep-index.moralis.io/api/v2/{wallet[Addr_Index]}/nft?chain={self._current_network.name}&format=decimal&token_addresses={self._contract.address}&normalizeMetadata=false"
        response = requests.get(url, headers=headers)
        nft_result = json.loads(response.text)

        if nft_result['total'] <= 0:
            print(f'No Nft found in Wallet {wallet[No_Index]} {wallet[Addr_Index]}, Ignored.')
            return

        print(f'Has Nft in Wallet {wallet[No_Index]} {wallet[Addr_Index]}.')
        if not is_transfer:
            return

        for each_result in nft_result['result']:
            token_id = int(each_result['token_id'])
            print(f'Start to Collect nft from Wallet {wallet[No_Index]} {wallet[Addr_Index]} {token_id}...')
            self.each_call_func(wallet, 'transferFrom',
                                (Web3.toChecksumAddress(wallet[Addr_Index]), Web3.toChecksumAddress(to_addr), token_id))

    def multi_transfer(self, from_wallet, csv_path, amount=0):
        wallets = []
        amounts = []
        total_value = 0

        callback = lambda wallet: {
            wallets.append(wallet[Addr_Index])
        }
        self.read_wallets_and_callback(csv_path, callback)

        for w in wallets:
            amount_wei = self._web3.toWei(amount, 'ether')
            amounts.append(amount_wei)
            total_value += amount_wei

        total_value += self._web3.toWei(0.001, 'ether')

        func_name = 'multisendEther'
        contract_func = self._contract.get_function_by_name(func_name)(wallets, amounts)
        self.call_contract_func(from_wallet, func_name, [wallets, amounts], contract_func, total_value)
