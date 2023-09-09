CREATE DATABASE estoque;

USE estoque;

CREATE TABLE estoque (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    quantidade INT NOT NULL
);

SELECT * FROM estoque;

DESCRIBE estoque;

SELECT * FROM estoque;
