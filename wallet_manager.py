from web3.eth import Account


def bytes_to_hex(bs):
    return ''.join(['%02X' % b for b in bs])


def create_new_wallet():
    Account.enable_unaudited_hdwallet_features()
    account = Account.create()
    privateKey = str.lower(bytes_to_hex(account.key))
    address = account.address
    return address, privateKey


def create_new_wallet_with_mnemonic():
    Account.enable_unaudited_hdwallet_features()
    create_result = Account.create_with_mnemonic()
    account = create_result[0]
    mnemonic = create_result[1]
    privateKey = str.lower(bytes_to_hex(account.key))
    address = account.address
    return address, privateKey, mnemonic
