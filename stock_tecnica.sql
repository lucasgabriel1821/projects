INSERT INTO usuarios (id, login, senha) VALUES
('1', 'lucas.gabriel', '28491');

SELECT* FROM usuarios;

UPDATE usuarios
SET coluna1 = usuario;

ALTER TABLE usuarios
CHANGE COLUMN nome usuario VARCHAR(255);

ALTER TABLE usuarios
DROP COLUMN email;

DESCRIBE usuarios;

ALTER TABLE usuarios
CHANGE COLUMN usuario usuario VARCHAR(255) NOT NULL;

SELECT * FROM usuarios;

INSERT INTO usuarios (id, usuario, senha) VALUES
('2', 'lucas.gabriel', '28491');

SELECT * FROM usuarios;

ALTER TABLE usuarios
ADD COLUMN senha INT;

ALTER TABLE usuarios
DROP COLUMN senha;

ALTER TABLE usuarios
ADD COLUMN senha INT;

DELETE FROM usuarios WHERE id = 2;

SELECT * FROM estoque;

DESCRIBE usuarios;

ALTER TABLE usuarios
DROP COLUMN senha;

ALTER TABLE usuarios
ADD COLUMN senha VARCHAR(10) NOT NULL;

INSERT INTO usuarios (id, usuario, senha) VALUES
('1', 'lucas.gabriel', '28491');

DROP TABLE usuarios;