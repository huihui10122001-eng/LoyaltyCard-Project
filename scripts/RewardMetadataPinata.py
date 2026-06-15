"""
RewardMetadataPinata.py
將集點卡系統中「獎品」的圖片與 metadata.json 上傳至 Pinata IPFS

執行前請先：
1. 註冊 Pinata 帳號 (https://pinata.cloud)
2. 於 API Keys 頁面建立一個具 Admin 權限的 API Key
3. 將下方 PINATA_API_KEY / PINATA_SECRET_API_KEY 換成自己的金鑰
4. 準備一張獎品圖片 reward.png 放在同一目錄下
"""

import requests
import json

PINATA_API_KEY = "your_pinata_api_key"
PINATA_SECRET_API_KEY = "your_pinata_secret_api_key"

headers = {
    "pinata_api_key": PINATA_API_KEY,
    "pinata_secret_api_key": PINATA_SECRET_API_KEY
}

# ---------- 1. 上傳獎品圖片 ----------
url_file = "https://api.pinata.cloud/pinning/pinFileToIPFS"

with open("reward.png", "rb") as fp:
    files = {'file': ("reward.png", fp)}
    res = requests.post(url_file, files=files, headers=headers)

print("圖片上傳結果:", res.status_code)
print(res.json())

image_hash = res.json()['IpfsHash']
image_url = f"https://gateway.pinata.cloud/ipfs/{image_hash}"
print("獎品圖片 URL =", image_url)

# ---------- 2. 建立並上傳 metadata.json ----------
metadata = {
    "name": "LoyaltyCard Reward - Coffee Voucher",
    "description": "可兌換一杯免費咖啡的數位集點獎品，學號 13363066",
    "image": image_url,
    "attributes": [
        {"trait_type": "Cost", "value": "10 LP"},
        {"trait_type": "Student ID", "value": "13363066"}
    ]
}

with open("reward_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

with open("reward_metadata.json", "rb") as fp:
    files = {'file': ("reward_metadata.json", fp)}
    res2 = requests.post(url_file, files=files, headers=headers)

print("metadata 上傳結果:", res2.status_code)
print(res2.json())

metadata_hash = res2.json()['IpfsHash']
print("Reward metadata URL =", f"https://gateway.pinata.cloud/ipfs/{metadata_hash}")
