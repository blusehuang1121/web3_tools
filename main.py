import xen_manager as xen
import wallet_manager as wal


def batch_claim_rank():
    x = xen.XenManager(xen.Network.eth)
    print('begin to batch claim rank')
    x.batch_claim_rank('wallets.csv', 300)


def batch_claim_mint_reward_and_share():
    x = xen.XenManager(xen.Network.eth)
    print('begin to batch claim mint reward and share')
    x.batch_claim_mint_reward_and_share('wallets.csv', '归集地址')


def update_all_mints():
    x = xen.XenManager(xen.Network.eth)
    x.update_all_mints('wallets.csv', 'xen_mint_data.csv')


def batch_transfer():
    from_wallet = [0, '转账地址', 'private_key']
    x = xen.XenManager(xen.Network.eth)
    x.transfer_money(0.004, from_wallet, 'wallets.csv')


if __name__ == '__main__':
    print('Demo batch functions for XEN')
    # 更新全部钱包的mint信息
    # update_all_mints()

    # 批量转账给小钱包
    # from_wallet = [0, '0xaddress', 'private_key']
    # x = xen.XenManager(xen.Network.eth)
    # x.transfer_money(0.004, from_wallet, 'wallets1.csv')
    # 批量mint
    # batch_claim_rank()

    # 批量获得代币并转移
    # batch_claim_mint_reward_and_share()
