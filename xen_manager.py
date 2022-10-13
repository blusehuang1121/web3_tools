import csv
import math
import time
from enum import Enum

from web3 import Web3
from web3.contract import Contract
from web3.gas_strategies.time_based import medium_gas_price_strategy
from web3.middleware import geth_poa_middleware


class Network(Enum):
    eth = 1,
    bsc = 2,
    goerli = 3


No_Index = 0
Addr_Index = 1
PriKey_Index = 2


# using https://chainlist.org to find the best RPC url
class XenManager:
    _xen_network_info = {
        Network.eth: {
            'addr': '0x06450dEe7FD2Fb8E39061434BAbCFC05599a6Fb8',
            'rpc': 'https://eth-mainnet.public.blastapi.io',
            'chain_id': 1,
            'gas_limit': 200000,
            'gas_price': 10,
            'max_fee_per_gas': 20,
            'max_priority_fee_per_gas': 1.5,
            'contract_abi': '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardAmount","type":"uint256"}],"name":"MintClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rank","type":"uint256"}],"name":"RankClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"}],"name":"Staked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"Withdrawn","type":"event"},{"inputs":[],"name":"AUTHORS","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DAYS_IN_YEAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_RANK_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GENESIS_RANK","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_PENALTY_PCT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_TERM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SECONDS_IN_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER_THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WITHDRAWAL_WINDOW_DAYS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_DAYS_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_BURN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_STAKE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeMinters","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeStakes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimMintReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"other","type":"address"},{"internalType":"uint256","name":"pct","type":"uint256"}],"name":"claimMintRewardAndShare","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"pct","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimMintRewardAndStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimRank","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"genesisTs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAMP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAPY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentEAAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentMaxTerm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rankDelta","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"eaa","type":"uint256"}],"name":"getGrossReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getUserMint","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"internalType":"struct XENCrypto.MintInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUserStake","outputs":[{"components":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"internalType":"struct XENCrypto.StakeInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"globalRank","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"stake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalXenStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userBurns","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userMints","outputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userStakes","outputs":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
        },
        Network.bsc: {
            'addr': '0x2AB0e9e4eE70FFf1fB9D67031E44F6410170d00e',
            'rpc': 'https://bscrpc.com',
            'chain_id': 56,
            'gas_limit': 300000,
            'gas_price': 5,
            'contract_abi': '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardAmount","type":"uint256"}],"name":"MintClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rank","type":"uint256"}],"name":"RankClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"}],"name":"Staked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"Withdrawn","type":"event"},{"inputs":[],"name":"AUTHORS","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DAYS_IN_YEAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_RANK_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GENESIS_RANK","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_PENALTY_PCT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_TERM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SECONDS_IN_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER_THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WITHDRAWAL_WINDOW_DAYS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_DAYS_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_BURN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_STAKE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeMinters","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeStakes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimMintReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"other","type":"address"},{"internalType":"uint256","name":"pct","type":"uint256"}],"name":"claimMintRewardAndShare","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"pct","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimMintRewardAndStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimRank","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"genesisTs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAMP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAPY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentEAAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentMaxTerm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rankDelta","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"eaa","type":"uint256"}],"name":"getGrossReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getUserMint","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"internalType":"struct XENCrypto.MintInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUserStake","outputs":[{"components":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"internalType":"struct XENCrypto.StakeInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"globalRank","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"stake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalXenStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userBurns","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userMints","outputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userStakes","outputs":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

        },
        Network.goerli: {
            'addr': '0xc78b129025A0877c75FDDa406E8908047092C582',
            'rpc': 'https://rpc.ankr.com/eth_goerli',
            'chain_id': 5,
            'gas_limit': 200000,
            'gas_price': 10,
            'max_fee_per_gas': 30,
            'max_priority_fee_per_gas': 1.5,
            'contract_abi': '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"rewardAmount","type":"uint256"}],"name":"MintClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rank","type":"uint256"}],"name":"RankClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"term","type":"uint256"}],"name":"Staked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"reward","type":"uint256"}],"name":"Withdrawn","type":"event"},{"inputs":[],"name":"AUTHORS","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DAYS_IN_YEAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_PM_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EAA_RANK_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"GENESIS_RANK","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_PENALTY_PCT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MAX_TERM_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_TERM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_AMPLIFIER_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SECONDS_IN_DAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"TERM_AMPLIFIER_THRESHOLD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WITHDRAWAL_WINDOW_DAYS","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_DAYS_STEP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_APY_START","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_BURN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"XEN_MIN_STAKE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeMinters","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activeStakes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"claimMintReward","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"other","type":"address"},{"internalType":"uint256","name":"pct","type":"uint256"}],"name":"claimMintRewardAndShare","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"pct","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimMintRewardAndStake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"term","type":"uint256"}],"name":"claimRank","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"genesisTs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAMP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentAPY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentEAAR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurrentMaxTerm","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"rankDelta","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"eaa","type":"uint256"}],"name":"getGrossReward","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"getUserMint","outputs":[{"components":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"internalType":"struct XENCrypto.MintInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getUserStake","outputs":[{"components":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"internalType":"struct XENCrypto.StakeInfo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"globalRank","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"term","type":"uint256"}],"name":"stake","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalXenStaked","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userBurns","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userMints","outputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"rank","type":"uint256"},{"internalType":"uint256","name":"amplifier","type":"uint256"},{"internalType":"uint256","name":"eaaRate","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userStakes","outputs":[{"internalType":"uint256","name":"term","type":"uint256"},{"internalType":"uint256","name":"maturityTs","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"apy","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

        }
    }

    _web3: Web3
    _xen_contract: Contract
    _gas_limit: int
    _gas_price: int
    _current_network: Network
    _max_fee_multiply = 1.5

    def __init__(self, network: Network = Network.eth) -> None:
        self._current_network = network
        network_info = self._xen_network_info[network]
        self._xen_rpc = network_info['rpc']
        self._xen_addr = network_info['addr']
        self._chain_id = network_info['chain_id']
        self._xen_abi = network_info['contract_abi']
        self._gas_limit = network_info['gas_limit']
        self._gas_price = network_info['gas_price']
        self._web3 = Web3(Web3.HTTPProvider(self._xen_rpc))
        if network == Network.bsc:
            self._web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self._xen_contract = self._web3.eth.contract(address=self._xen_addr, abi=self._xen_abi)
        self._web3.eth.set_gas_price_strategy(medium_gas_price_strategy)

        self._max_fee_per_gas = self._web3.eth.max_priority_fee + int(
            self._max_fee_multiply * self._web3.eth.get_block('latest')['baseFeePerGas'])
        self._max_priority_fee_per_gas = self._web3.eth.max_priority_fee

    def get_global_rank(self) -> int:
        return self._xen_contract.functions.globalRank().call()

    def get_mint_info(self, addr):
        return self._xen_contract.functions.userMints(addr).call()

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

    @staticmethod
    def cal_estimated_xen(term, global_rank, rank, amp, eaa):
        return term * math.log2(global_rank - rank) * amp * (1 + eaa / 1000)

    def update_all_mints(self, csv_path, info_csv_path):
        info_datas = []
        global_rank = self.get_global_rank()
        with open(csv_path) as f:
            f_csv = csv.reader(f)
            headers = next(f_csv)
            row_no = 1
            for each_wallet in f_csv:
                self.handle_each_wallet(each_wallet, info_datas, global_rank, row_no)
                row_no += 1

        self.write_info_to_file(info_datas, info_csv_path)

    def handle_each_wallet(self, each_wallet, info_datas, global_rank, row_no):
        addr = each_wallet[Addr_Index]
        mint_info = self.get_mint_info(addr)
        term = mint_info[1]
        maturityTs = mint_info[2]
        rank = mint_info[3]
        amp = mint_info[4]
        eaa = mint_info[5]

        if rank == 0:
            return
        xen_count = self.cal_estimated_xen(term, global_rank, rank, amp, eaa)
        mint_info_data = [row_no, addr, term, self.local_time(maturityTs), int(xen_count)]
        print(mint_info_data)
        info_datas.append(mint_info_data)

    def each_claim_rank(self, wallet, term):
        func_name = 'claimRank'
        func_args = [term]
        contract_func = self._xen_contract.functions.claimRank(term)
        try:
            self.call_contract_func(wallet, func_name, func_args, contract_func)
        except Exception as e:
            print(f'claimRank has an error {wallet[Addr_Index]}, {repr(e)}')

    def call_contract_func(self, wallet, func_name, func_args, contract_func):
        addr = wallet[Addr_Index]
        private_key = wallet[PriKey_Index]

        if len(private_key.strip()) <= 0:
            print(f'{addr} private key is empty, ignored.')
            return

        encodedData = self._xen_contract.encodeABI(fn_name=func_name, args=func_args)
        trans_params = {
            'chainId': self._chain_id,
            "from": addr,
            'to': self._xen_addr,
            "nonce": self._web3.eth.getTransactionCount(addr),
            'data': encodedData
        }
        self.update_mint_gas(contract_func, trans_params)
        print(f'Start to {func_name} {addr} {trans_params}')
        signed_tx = self._web3.eth.account.signTransaction(trans_params, private_key=private_key)
        tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f'Transaction sent to chain...{tx_hash}')
        # receipt = self._web3.eth.waitForTransactionReceipt(tx_hash)
        # print("Transaction receipt mined: \n")
        # print(dict(receipt))
        # print("Was transaction successful? \n")
        # print(receipt['status'])

    def each_claim_mint_reward_and_share(self, wallet, to_addr):
        mint_info = self.get_mint_info(wallet[Addr_Index])
        maturityTs = mint_info[2]
        if maturityTs <= 0:
            print(f'Wallet {wallet[Addr_Index]} not minted XEN, ignored.')
            return

        current_time = int(time.time())
        if current_time < maturityTs:
            print(f'Wallet {wallet[Addr_Index]} claim XEN Not available, ignored.')
            return

        func_name = 'claimMintRewardAndShare'
        percent = 100
        to_addr = Web3.toChecksumAddress(to_addr)
        func_args = [to_addr, percent]
        contract_func = self._xen_contract.functions.claimMintRewardAndShare(to_addr, percent)

        try:
            self.call_contract_func(wallet, func_name, func_args, contract_func)
        except Exception as e:
            print(f'claimMintRewardAndShare has an error {wallet[Addr_Index]}, {repr(e)}')


    def update_mint_gas(self, contract_func, trans_params):
        estimate_param = {
            'chainId': trans_params['chainId'],
            'from': trans_params['from']
        }
        trans_params['gas'] = contract_func.estimate_gas(estimate_param)

        if self._current_network in [Network.eth, Network.goerli]:
            trans_params['maxFeePerGas'] = self._max_fee_per_gas  # self._web3.toWei(self._max_fee_per_gas, 'gwei')
            trans_params[
                'maxPriorityFeePerGas'] = self._max_priority_fee_per_gas  # self._web3.toWei(self._max_priority_fee_per_gas, 'gwei')
        else:
            trans_params['gasPrice'] = self._web3.eth.gas_price

    def read_wallets_and_callback(self, csv_path, callback):
        with open(csv_path) as f:
            f_csv = csv.reader(f)
            next(f_csv)
            for each_wallet in f_csv:
                callback(each_wallet)

    def batch_claim_rank(self, csv_path, term):
        callback = lambda wallet: {
            self.each_claim_rank(wallet, term)
        }
        self.read_wallets_and_callback(csv_path, callback)

    def batch_claim_mint_reward_and_share(self, csv_path, share_addr):
        callback = lambda wallet: {
            self.each_claim_mint_reward_and_share(wallet, share_addr)
        }
        self.read_wallets_and_callback(csv_path, callback)

    def is_connect(self):
        return self._web3.isConnected()

    def transfer_money(self, amount, from_wallet, csv_path):
        to_wallets = []
        callback = lambda wallet: {
            to_wallets.append(wallet)
        }
        self.read_wallets_and_callback(csv_path, callback)

        for to_wallet in to_wallets:
            print(f'Transferring {amount} from {from_wallet[Addr_Index]} to {to_wallet[Addr_Index]}')
            from_addr = from_wallet[Addr_Index]
            to_addr = to_wallet[Addr_Index]
            if from_addr == to_addr:
                continue
            nonce = self._web3.eth.get_transaction_count(from_addr)
            params = {
                'chainId': self._chain_id,
                'nonce': nonce,
                'from': from_addr,
                'to': to_wallet[Addr_Index],
                'value': self._web3.toWei(amount, 'ether'),
                'gas': self._gas_limit,
                'maxFeePerGas': self._max_fee_per_gas,
                'maxPriorityFeePerGas': self._max_priority_fee_per_gas
            }
            signed_tx = self._web3.eth.account.sign_transaction(params, private_key=from_wallet[PriKey_Index])
            tx_hash = self._web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f'Eth Transfer sent to chain...{tx_hash}')
            self._web3.eth.waitForTransactionReceipt(tx_hash)
