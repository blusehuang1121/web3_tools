# web3_tools 简要说明

### 准备工作
&ensp;&ensp;安装web3组件
`pip install web3`

### 如何创建钱包
```
import wallet_manager as wal
wal_info = wal.create_new_wallet()
```
wal_info包含三个字段，序号、地址、私钥

### 如何批量转账
```
#转账的母钱包，使用该钱包的余额给其他子钱包转账
from_wallet = [0, '转账地址', '私钥'] 
    
#给csv文件中的所有钱包转账，金额0.001
manager.transfer_money(0.001, from_wallet, 'xxx.csv')
```

### 如何批量获得余额
```
manager.batch_get_balance('xxx.csv')
```

### 如何批量操作XEN
+ 选择网络并实例化（暂时只支持bsc、eth）
`manager = xen.XenManager(Network.eth)`
+ 调用批量方法
`manager.batch_claim_rank('xxx.csv', 天数)`
+ 获得最大的ClaimRank天数
`manager.get_max_term_days()`
+ 到期后可批量Claim然后归集到统一的地址
`manager.batch_claim_mint_reward_and_share('xxx.csv', 归集地址)`
+ 更新钱包的XEN信息（到期时间、数量等）
`manager.update_all_mints('xxx.csv', 'data.csv')`

### 如何多钱包调用合约，例如Mint
+ 需要制定合约的地址和abi（拿猫头鹰举例）
```
network_data = {
    Network.eth: {
        'addr': '0xdd44443d8A3563E947EAd8A2254b36f8D8b28581',
        'contract_abi': '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ApprovalCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"ApprovalQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"BalanceQueryForZeroAddress","type":"error"},{"inputs":[],"name":"MintERC2309QuantityExceedsLimit","type":"error"},{"inputs":[],"name":"MintToZeroAddress","type":"error"},{"inputs":[],"name":"MintZeroQuantity","type":"error"},{"inputs":[],"name":"OwnerQueryForNonexistentToken","type":"error"},{"inputs":[],"name":"OwnershipNotInitializedForExtraData","type":"error"},{"inputs":[],"name":"TransferCallerNotOwnerNorApproved","type":"error"},{"inputs":[],"name":"TransferFromIncorrectOwner","type":"error"},{"inputs":[],"name":"TransferToNonERC721ReceiverImplementer","type":"error"},{"inputs":[],"name":"TransferToZeroAddress","type":"error"},{"inputs":[],"name":"URIQueryForNonexistentToken","type":"error"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"approved","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"operator","type":"address"},{"indexed":false,"internalType":"bool","name":"approved","type":"bool"}],"name":"ApprovalForAll","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"uint256","name":"fromTokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"toTokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"ConsecutiveTransfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"Received","type":"event"},{"anonymous":false,"inputs":[{"components":[{"internalType":"uint64","name":"stageNum","type":"uint64"},{"internalType":"uint64","name":"maxPerStage","type":"uint64"},{"internalType":"uint64","name":"maxPerAddress","type":"uint64"},{"internalType":"bool","name":"isWhiteListMintActive","type":"bool"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"bool","name":"isPublicMintActive","type":"bool"}],"indexed":false,"internalType":"struct Owl.StageMintConfig","name":"config","type":"tuple"}],"name":"StageMintConfigChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"addressMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"approve","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"getApproved","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"operator","type":"address"}],"name":"isApprovedForAll","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"address_","type":"address"},{"internalType":"bytes32[]","name":"merkleProof","type":"bytes32[]"}],"name":"isKYCAddress","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"quantity","type":"uint64"}],"name":"publicMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"salePrice","type":"uint256"}],"name":"royaltyInfo","outputs":[{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint256","name":"royaltyAmount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"safeTransferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"operator","type":"address"},{"internalType":"bool","name":"approved","type":"bool"}],"name":"setApprovalForAll","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_kycMerkleRoot","type":"bytes32"}],"name":"setKycMerkleRoot","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"newMaxPerAddress","type":"uint64"}],"name":"setMaxPerAddress","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"newMaxPerStage","type":"uint64"}],"name":"setMaxPerStage","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"mintStarted","type":"bool"}],"name":"setPublicMintActive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"stageNum","type":"uint64"},{"internalType":"uint64","name":"maxPerStage","type":"uint64"},{"internalType":"uint64","name":"maxPerAddress","type":"uint64"},{"internalType":"bool","name":"isWhiteListMintActive","type":"bool"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"bool","name":"isPublicMintActive","type":"bool"}],"internalType":"struct Owl.StageMintConfig","name":"config_","type":"tuple"}],"name":"setStageMintConfig","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"tokenURI_","type":"string"}],"name":"setTokenURI","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"mintStarted","type":"bool"}],"name":"setWhiteListMintActive","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stageMintConfig","outputs":[{"internalType":"uint64","name":"stageNum","type":"uint64"},{"internalType":"uint64","name":"maxPerStage","type":"uint64"},{"internalType":"uint64","name":"maxPerAddress","type":"uint64"},{"internalType":"bool","name":"isWhiteListMintActive","type":"bool"},{"internalType":"bytes32","name":"merkleRoot","type":"bytes32"},{"internalType":"bool","name":"isPublicMintActive","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"tokenURI","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalMinted","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"transferFrom","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"quantity","type":"uint64"},{"internalType":"bytes32[]","name":"merkleProof","type":"bytes32[]"}],"name":"whitelistMint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdraw","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"contract IERC20","name":"token","type":"address"}],"name":"withdrawTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
    }
}
```
+ 制定合约的方法名和参数，调用批量方法
```
manager = BatchMintManager(Network.eth, network_data)
manager.batch_call_write_func('xxx.csv', 'publicMint', (1))
```
+ 如果需要，可以不使用动态gas，而通过调用limit_gas方法指定gas限制

***

##### *XEN的示例代码参考main.py*
##### *批量Mint猫头鹰的实例代码参考batch_func_runner.py*
