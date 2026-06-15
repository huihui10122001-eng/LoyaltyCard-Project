"""
QueryLoyaltyPoints.py
透過 Web3.py 連線至 Sepolia 測試網，查詢指定錢包的 LoyaltyToken (LP) 點數餘額

執行前請先：
1. pip install web3
2. 將 CONTRACT_ADDRESS 換成自己部署的合約地址
3. 將 WALLET_ADDRESS 換成欲查詢的錢包地址
"""

from web3 import Web3

# 連接到 Sepolia 公開節點
w3 = Web3(Web3.HTTPProvider("https://ethereum-sepolia.publicnode.com"))

# LoyaltyToken 合約地址（部署後填入）
CONTRACT_ADDRESS = "0xYourContractAddress"

# 欲查詢的錢包地址
WALLET_ADDRESS = "0xYourWalletAddress"

# 合約 ABI（僅列出本程式需要呼叫的函式）
abi = [
    {
        "constant": True,
        "inputs": [{"name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=abi
)

token_name = contract.functions.name().call()
token_symbol = contract.functions.symbol().call()
balance = contract.functions.balanceOf(
    Web3.to_checksum_address(WALLET_ADDRESS)
).call()

print(f"代幣名稱: {token_name} ({token_symbol})")
print(f"錢包地址: {WALLET_ADDRESS}")
print(f"目前點數餘額: {balance} {token_symbol}")
