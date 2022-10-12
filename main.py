# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import xen_manager as xen

if __name__ == '__main__':
    print('begin to update mint infos')
    xen.update_all_mints('wallets.csv', 'xen_mint_data.csv')
