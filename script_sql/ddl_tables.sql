CREATE TABLE pessoa (
    id_pessoa SERIAL PRIMARY KEY,
    nome VARCHAR(1000) NOT NULL,
    nascimento DATE,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    dt_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE arquivos (
    id_arquivo SERIAL PRIMARY KEY,
    id_pessoa INTEGER REFERENCES pessoa(id_pessoa),
    path VARCHAR(1000) NOT NULL
);