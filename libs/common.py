import os

PROJECT_ABSOLUTE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPLACE_WALLET_ADDR = '$ReplaceWallet$'

def get_file_path(f_path):
    return os.path.join(PROJECT_ABSOLUTE_PATH, f_path)
