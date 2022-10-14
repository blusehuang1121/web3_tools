import xen_manager as xen
import wallet_manager as wal

current_network = xen.Network.eth

def batch_claim_rank():
    x = xen.XenManager(current_network)
    print('begin to batch claim rank')
    x.batch_claim_rank('wallets.csv', 300)


def batch_claim_mint_reward_and_share():
    x = xen.XenManager(current_network)
    print('begin to batch claim mint reward and share')
    x.batch_claim_mint_reward_and_share('wallets.csv', '归集地址')


def update_all_mints():
    x = xen.XenManager(current_network)
    x.update_all_mints('wallets.csv', f'xen_mint_data_{x._current_network}.csv')


def batch_get_balance():
    x = xen.XenManager(current_network)
    x.batch_get_balance('wallets.csv')


def batch_transfer():
    from_wallet = [0, '转账地址', '私钥']
    x = xen.XenManager(xen.Network.eth)
    x.transfer_money(0.001, from_wallet, 'wallets.csv')


if __name__ == '__main__':
    print('Demo batch functions for XEN')
    current_network = xen.Network.bsc
    # 更新全部钱包的mint信息
    # update_all_mints()

    # 批量获得钱包余额
    # batch_get_balance()

    # 批量转账给小钱包
    #batch_transfer()

    # 批量mint
    # batch_claim_rank()

    # 批量获得代币并转移
    # batch_claim_mint_reward_and_share()
