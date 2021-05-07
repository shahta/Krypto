CREATE TABLE `wallets` (
   `FirstName` varchar(255) NOT NULL,
   `LastName` varchar(255) NOT NULL,
   `Email` varchar(255) NOT NULL,
   `EncPassword` varchar(255) NOT NULL,
   `Coins` FLOAT,
   `WalletAddress` varchar(255) NOT NULL,
   PRIMARY KEY (`WalletAddress`)
 ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci