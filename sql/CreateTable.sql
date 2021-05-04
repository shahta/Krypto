CREATE TABLE Wallets (
    ID int AUTO_INCREMENT,
    FirstName varchar(255) NOT NULL,
    LastName varchar(255) NOT NULL,
    Email varchar(255) NOT NULL,
    EncPassword varchar(255) NOT NULL,
    WalletAddress varchar(255) NOT NULL,
    PRIMARY KEY (ID, WalletAddress)
);