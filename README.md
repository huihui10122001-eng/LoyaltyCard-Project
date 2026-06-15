# 區塊鏈數位集點卡系統
## Blockchain Digital Loyalty Card System

學號：13363066
課程：區塊鏈技術 期末專題

---

## 專題簡介

本專題利用 **以太坊智能合約（ERC20）** 與 **IPFS 去中心化儲存**，
打造一套去中心化的數位集點卡系統，解決傳統實體集點卡容易遺失、偽造、
無法跨店通用、缺乏透明度等問題。

系統核心概念：

1. 商家部署 **LoyaltyToken**（ERC20 集點代幣）智能合約
2. 商家可發行點數（`issuePoints`）給消費者
3. 商家可新增獎品（`addReward`），獎品圖片與資訊存放於 IPFS
4. 消費者可使用點數兌換獎品（`redeem`）
5. 所有點數發行、轉移、兌換紀錄皆公開於鏈上，不可竄改

---

## 系統架構

```
[ 商家 Owner ]                [ LoyaltyToken 智能合約 (ERC20) ]              [ 消費者 User ]
                                                                                  
部署合約 ───────────────────▶  發行 LoyaltyPoint (LP) 代幣
                                                                                  
issuePoints(to, amount) ───▶  將點數轉入消費者錢包  ─────────────────────▶  累積點數

addReward(name, cost,
  stock, metadataURI)  ────▶  新增獎品（圖片存於 IPFS）

                                                          redeem(rewardId) ◀──── 消費者兌換獎品
                                                                │
                                                          扣除點數 + 庫存-1
                                                                │
                                                          鏈上紀錄 RewardRedeemed 事件


      [ IPFS / Pinata ]
      儲存獎品圖片 & metadata.json
```

---

## 專案結構

```
LoyaltyCard-Project/
├── contracts/
│   └── LoyaltyToken.sol          # ERC20 集點卡智能合約原始碼
├── scripts/
│   ├── RewardMetadataPinata.py    # 上傳獎品圖片與 metadata 至 Pinata IPFS
│   └── QueryLoyaltyPoints.py      # Web3.py 查詢點數餘額
├── screenshots/                   # 各步驟執行結果截圖
└── README.md
```

---

## 智能合約功能說明

| 函式 | 權限 | 說明 |
|------|------|------|
| `constructor(initialSupply)` | - | 部署時發行初始點數給合約擁有者（商家） |
| `issuePoints(to, amount)` | onlyOwner | 商家發行點數給指定消費者 |
| `addReward(name, cost, stock, metadataURI)` | onlyOwner | 新增可兌換獎品 |
| `redeem(rewardId)` | 任何持有者 | 消費者使用點數兌換獎品 |
| `balanceOf(account)` | 任何人 | 查詢點數餘額（ERC20 標準函式） |
| `rewardCount()` | 任何人 | 取得目前獎品總數 |

---

## 編譯與執行說明

### 1. 部署智能合約（Remix + MetaMask）

1. 開啟 [Remix IDE](https://remix.ethereum.org)
2. 新增檔案 `LoyaltyToken.sol`，貼上 `contracts/LoyaltyToken.sol` 程式碼
3. Solidity Compiler 版本選擇 **0.8.20 以上**，並完成編譯
4. Deploy & Run Transactions：
   - Environment 選擇 **Browser Extension (MetaMask)**
   - 確認 MetaMask 已切換至 **Sepolia 測試網路**，且帳號有測試用 SepoliaETH
   - 於建構子參數 `initialSupply` 輸入初始發行點數，例如 `1000000000000000000000`（1000 LP，因 ERC20 預設 18 位小數）
   - 點擊 **Deploy**，於 MetaMask 確認交易

### 2. 發行點數給消費者

1. 部署成功後，於 Deployed Contracts 展開合約
2. 呼叫 `issuePoints`：
   - `to`：消費者錢包地址
   - `amount`：欲發行的點數數量（含 18 位小數，例如 10 點 = `10000000000000000000`）
3. 點擊 **transact**，於 MetaMask 確認交易

### 3. 上傳獎品圖片與 metadata 至 IPFS

1. 註冊 [Pinata](https://pinata.cloud) 帳號，取得 Admin 權限的 API Key
2. 修改 `scripts/RewardMetadataPinata.py` 的 API Key 與 Secret
3. 準備一張獎品圖片 `reward.png`
4. 執行：

```bash
pip install requests
python RewardMetadataPinata.py
```

5. 程式會輸出獎品圖片與 metadata 的 IPFS URL

### 4. 新增獎品

1. 於 Remix 呼叫 `addReward`：
   - `name`：獎品名稱，例如 `"Coffee Voucher"`
   - `cost`：兌換所需點數，例如 `10000000000000000000`（10 LP）
   - `stock`：庫存數量，例如 `5`
   - `metadataURI`：步驟 3 取得的 IPFS URL
2. 點擊 **transact** 完成新增

### 5. 兌換獎品

消費者於 Remix（切換為消費者帳號）呼叫 `redeem(rewardId)`，
即可使用點數兌換對應獎品，合約會自動扣除點數並更新庫存。

### 6. 查詢點數餘額（Python DApp）

1. 修改 `scripts/QueryLoyaltyPoints.py` 中的 `CONTRACT_ADDRESS` 與 `WALLET_ADDRESS`
2. 執行：

```bash
pip install web3
python QueryLoyaltyPoints.py
```

3. 程式會顯示代幣名稱、符號與目前點數餘額

### 7. 驗證成果

於 [Sepolia Etherscan](https://sepolia.etherscan.io) 輸入合約地址或錢包地址，
即可查詢 `LoyaltyPoint (LP)` 代幣的發行、轉移與兌換紀錄。

---

## 使用工具與技術

| 類別 | 工具 / 技術 |
|------|------|
| 區塊鏈平台 | Ethereum Sepolia Testnet |
| 智能合約 | Solidity (ERC20, OpenZeppelin) |
| 開發工具 | Remix IDE |
| 錢包 | MetaMask |
| 去中心化儲存 | IPFS / Pinata |
| Python DApp | web3.py / requests |

---

## 合約地址 (Sepolia)

```
0xd2265fCBC1678Ec70b40dB3da33C5149aE444838
```

可於 Etherscan 查詢：
https://sepolia.etherscan.io/address/<your_contract_address>
