import csv
import random
import time

from web3 import Web3

from core.batch_manager import Network
from core.tool_helper import ToolHelper
from libs.common import REPLACE_WALLET_ADDR
from libs.global_config import GlobalConfig


def get_random_amount(amount):
    return amount + (random.randrange(-10, 10) / 100) * amount


usdc_contract_addr = '0x80732890c93c6D9c6C23E06F888eD0CB88A06018'
weth_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deposit","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"},{"name":"","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Deposit","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Withdrawal","type":"event"}]'
weth_contract_addr = '0x05fDbDfaE180345C6Cff5316c286727CF1a43327'
uniswap_router_abi = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
swap_contract_addr = '0xEe0e03C1a621084cA3c542F36E4A5D0230304471'
l1_bridge_amount = get_random_amount(0.005)
l2_bridge_amount = get_random_amount(0.004)


def interact_single_wallet_with_zksync(base_wallet, to_wallet):
    # Transfer Eth to wallets in csv file
    print('*************开始转账到小钱包****************')
    ToolHelper().contract('0x60371a3af7eA5A1cE594de2E419FF942134B1F70') \
        .abi('[]') \
        .network(Network.zksync_testnet) \
        .wait_for_complete(True) \
        .transfer_eth_single(get_random_amount(0.01), base_wallet, to_wallet)

    # # Bridge from L1 to L2
    # # L1 bridge contract[0x94Cf11667B017e9Fef7Ab557E2eF9EFf6fdfeDc3 ]
    # print('*************开始跨链，从L1到L2****************')
    # bridge_abi = '[{"inputs":[{"internalType":"uint256","name":"num","type":"uint256"}],"name":"depositETH","outputs":[],"stateMutability":"payable","type":"function"}]'
    # ToolHelper().contract('0x94Cf11667B017e9Fef7Ab557E2eF9EFf6fdfeDc3') \
    #     .abi(bridge_abi) \
    #     .network(Network.scroll_test_l1) \
    #     .value(l1_bridge_amount) \
    #     .gas_limit(130000) \
    #     .gas_max_fee(1.5) \
    #     .gas_priority_fee(1.5) \
    #     .wallet(to_wallet) \
    #     .wait_for_complete(True) \
    #     .call_write('depositETH', (0))


def interact_single_wallet_with_scroll_l2(to_wallet):
    approve_usdc_in_l2(to_wallet)

    bridge_l2_to_l1(to_wallet)

    swap_from_eth_to_weth(to_wallet)

    swap_from_eth_to_usdc(to_wallet)

    add_liquidity_eth_usdc(to_wallet)


def add_liquidity_eth_usdc(to_wallet):
    # Step 2, make swap TSETH to TSUSDC
    print('*************增加流动性 ETH/USDC****************')
    liquidity_amount = 0.0005
    amount_in = Web3.toWei(liquidity_amount, 'ether')
    swap_path = [weth_contract_addr, usdc_contract_addr]
    amount_path_out = ToolHelper().contract(swap_contract_addr) \
        .abi(uniswap_router_abi) \
        .network(Network.scroll_test_l2) \
        .wallet(to_wallet) \
        .call_read('getAmountsOut', (amount_in, swap_path))
    amount_out = amount_path_out[1]
    deadline = int(time.time() + 60)
    ToolHelper().contract(swap_contract_addr) \
        .abi(uniswap_router_abi) \
        .value(liquidity_amount) \
        .network(Network.scroll_test_l2) \
        .gas_limit(200000) \
        .gas_max_fee(1.5) \
        .gas_priority_fee(1.5) \
        .wallet(to_wallet) \
        .call_write('addLiquidityETH', (
        Web3.to_checksum_address('0x80732890c93c6D9c6C23E06F888eD0CB88A06018'), amount_out, 0, 0, REPLACE_WALLET_ADDR,
        deadline))


def swap_from_eth_to_usdc(to_wallet):
    # Make swap in L2
    # Step1, get TSUSDC amount out
    # uniswap contract [0xEe0e03C1a621084cA3c542F36E4A5D0230304471]
    # TSUSDC contract [0x80732890c93c6D9c6C23E06F888eD0CB88A06018]
    print('*************开始Swap，把ETH换成USDC****************')
    swap_eu = l2_bridge_amount / 5
    amount_in = Web3.to_wei(swap_eu, 'ether')
    swap_path = [weth_contract_addr, usdc_contract_addr]
    amount_path_out = ToolHelper().contract(swap_contract_addr) \
        .abi(uniswap_router_abi) \
        .network(Network.scroll_test_l2) \
        .wallet(to_wallet) \
        .call_read('getAmountsOut', (amount_in, swap_path))
    # Step 2, make swap TSETH to TSUSDC
    amount_out = amount_path_out[1]
    deadline = int(time.time() + 60)
    ToolHelper().contract(swap_contract_addr) \
        .abi(uniswap_router_abi) \
        .value(swap_eu) \
        .network(Network.scroll_test_l2) \
        .gas_limit(200000) \
        .gas_max_fee(1.5) \
        .gas_priority_fee(1.5) \
        .wallet(to_wallet) \
        .wait_for_complete(True) \
        .call_write('swapExactETHForTokens', (amount_out, swap_path, REPLACE_WALLET_ADDR, deadline))


def swap_from_eth_to_weth(to_wallet):
    # Wrap ether in L2
    # WETH contract [0x05fDbDfaE180345C6Cff5316c286727CF1a43327]
    print('*************开始Swap，把ETH换成WETH****************')
    ToolHelper().contract(weth_contract_addr) \
        .abi(weth_abi) \
        .network(Network.scroll_test_l2) \
        .value(l2_bridge_amount / 6) \
        .gas_limit(50000) \
        .gas_max_fee(1.5) \
        .gas_priority_fee(1.5) \
        .wallet(to_wallet) \
        .wait_for_complete(True) \
        .call_write('deposit', ())


def bridge_l2_to_l1(to_wallet):
    # Bridge from L2 to L1
    # L2 bridge contract[0x8318ed43dD6760dA6A01B7605C408841e7062419]
    print('*************开始跨链，从L2到L1****************')
    bridge_abi = '[{"inputs":[{"internalType":"uint256","name":"num","type":"uint256"}],"name":"withdrawETH","outputs":[],"stateMutability":"payable","type":"function"}]'
    ToolHelper().contract('0x8318ed43dD6760dA6A01B7605C408841e7062419') \
        .abi(bridge_abi) \
        .network(Network.scroll_test_l2) \
        .value(l2_bridge_amount / 10) \
        .gas_limit(200000) \
        .gas_max_fee(1.5) \
        .gas_priority_fee(1.5) \
        .wallet(to_wallet) \
        .wait_for_complete(True) \
        .call_write('withdrawETH', (0))


def approve_usdc_in_l2(to_wallet):
    print('*************APPROVE USDC to SWAP****************')
    ToolHelper().contract(usdc_contract_addr) \
        .abi(
        '[{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]') \
        .network(Network.scroll_test_l2) \
        .gas_limit(200000) \
        .gas_max_fee(1.5) \
        .gas_priority_fee(1.5) \
        .wallet(to_wallet) \
        .wait_for_complete(True) \
        .call_write('approve', (
        Web3.to_checksum_address('0xEe0e03C1a621084cA3c542F36E4A5D0230304471'), Web3.to_wei(2 ** 64 - 1, 'ether')))


def batch_transfer_to_wallets_from(from_wallet, wallets_file):
    result_f = open('zksync_failed_result.txt', 'w')
    with open(wallets_file) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for each_wallet in f_csv:
            try:
                interact_single_wallet_with_zksync(from_wallet, each_wallet)
            except Exception as e:
                print(f'interact zksync error {repr(e)}')
                result_f.write(','.join(each_wallet))
                result_f.write('\n')
                result_f.flush()


def interact_wallets_with_zksync(from_wallet, wallets_file):
    result_f = open('zksync_failed_result.txt', 'w')
    with open(wallets_file) as f:
        f_csv = csv.reader(f)
        next(f_csv)
        for each_wallet in f_csv:
            interact_single_wallet_with_zksync(from_wallet, each_wallet)
            try:
                pass
                # GlobalConfig().use_proxy()
                # GlobalConfig().random_proxy()
            except Exception as e:
                print(f'interact zksync error {repr(e)}')
                result_f.write(','.join(each_wallet))
                result_f.write('\n')
                result_f.flush()
                # result_f.write(f"Failed! Wallet {each_wallet[0]} interact scroll l1\n")

    # with open(wallets_file) as f:
    #     f_csv = csv.reader(f)
    #     next(f_csv)
    #     for each_wallet in f_csv:
    #         try:
    #             GlobalConfig().use_proxy()
    #             GlobalConfig().random_proxy()
    #             interact_single_wallet_with_scroll_l2(each_wallet)
    #             # add_liquidity_eth_usdc(each_wallet)
    #         except Exception as e:
    #             print(f'interact scroll l2 error {repr(e)}')
    #             # result_f.write(f"Failed! Wallet {each_wallet[0]} interact scroll l2\n")
    #             result_f.write(','.join(each_wallet))
    #             result_f.write('\n')
    #             result_f.flush()
    result_f.close()


if __name__ == '__main__':
    print('Begin zksync testnet interact...')
    # 批量操作zksync testnet, https://portal.zksync.io/

    with open('xen_mints/base_transfer_wallet.csv') as f:
        reader = csv.reader(f)
        from_wallet = list(reader)[1]

    batch_transfer_to_wallets_from(from_wallet, 'xen_mints/wallets_tomint.csv')


