// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/// @title LoyaltyToken - 區塊鏈數位集點卡系統
/// @notice 以 ERC20 代幣作為數位點數，支援商家發行點數與消費者兌換獎品
/// @dev 部署於 Ethereum Sepolia 測試網，學號 13363066
contract LoyaltyToken is ERC20, Ownable {

    /// @notice 獎品結構
    struct Reward {
        string name;        // 獎品名稱
        uint256 cost;       // 兌換所需點數
        uint256 stock;      // 庫存數量
        string metadataURI; // 獎品圖片 / metadata 的 IPFS URI
    }

    // 獎品清單
    Reward[] public rewards;

    // 紀錄使用者已兌換的獎品次數 user => rewardId => count
    mapping(address => mapping(uint256 => uint256)) public redemptions;

    event RewardAdded(uint256 rewardId, string name, uint256 cost, uint256 stock);
    event RewardRedeemed(address indexed user, uint256 rewardId, string name);
    event PointsIssued(address indexed to, uint256 amount);

    constructor(uint256 initialSupply)
        ERC20("LoyaltyPoint", "LP")
        Ownable(msg.sender)
    {
        // 初始發行點數給合約擁有者（商家）
        _mint(msg.sender, initialSupply);
    }

    /// @notice 商家發行點數給消費者（僅限擁有者）
    /// @param to 接收點數的消費者地址
    /// @param amount 發行的點數數量
    function issuePoints(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
        emit PointsIssued(to, amount);
    }

    /// @notice 新增可兌換獎品（僅限擁有者）
    /// @param name 獎品名稱
    /// @param cost 兌換所需點數
    /// @param stock 獎品庫存數量
    /// @param metadataURI 獎品 metadata 的 IPFS URI
    function addReward(
        string memory name,
        uint256 cost,
        uint256 stock,
        string memory metadataURI
    ) external onlyOwner {
        rewards.push(Reward(name, cost, stock, metadataURI));
        emit RewardAdded(rewards.length - 1, name, cost, stock);
    }

    /// @notice 取得獎品總數
    function rewardCount() external view returns (uint256) {
        return rewards.length;
    }

    /// @notice 使用點數兌換獎品
    /// @param rewardId 獎品編號
    function redeem(uint256 rewardId) external {
        require(rewardId < rewards.length, "Invalid reward");
        Reward storage r = rewards[rewardId];

        require(r.stock > 0, "Out of stock");
        require(balanceOf(msg.sender) >= r.cost, "Not enough points");

        // 將點數轉回給合約擁有者（消耗點數）
        _transfer(msg.sender, owner(), r.cost);

        r.stock -= 1;
        redemptions[msg.sender][rewardId] += 1;

        emit RewardRedeemed(msg.sender, rewardId, r.name);
    }
}
