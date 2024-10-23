CREATE SCHEMA biblioteca;
CREATE DOMAIN status_dom AS VARCHAR(3)
CHECK (VALUE IN ('ATV', 'INA', 'RES'));
CREATE DOMAIN cod_usuario_domain AS VARCHAR(30)
CHECK (VALUE ~ '^[A-Za-z0-9]+$');


CREATE TABLE biblioteca.secao (
    cod_secao VARCHAR(30),
    nome VARCHAR(45) NOT NULL,
    CONSTRAINT pk_secao PRIMARY KEY (cod_secao)
);

CREATE TABLE biblioteca.contato (
    email VARCHAR(40),
    telefone VARCHAR(12) NOT NULL,
	cep VARCHAR(8) NOT NULL,
	rua VARCHAR(255) NOT NULL,
	bairro VARCHAR(60),
	cidade VARCHAR(60) NOT NULL,
	estado VARCHAR(60) NOT NULL,
	pais VARCHAR(60) NOT NULL,
    CONSTRAINT pk_contato PRIMARY KEY (email),
  	CONSTRAINT uq_endereco UNIQUE (cep, rua, bairro, cidade, estado)
);

CREATE TABLE biblioteca.genero (
    cod_genero INT,
    nome VARCHAR(45) NOT NULL,
    CONSTRAINT pk_genero PRIMARY KEY (cod_genero)
);

CREATE TABLE biblioteca.categoria (
    cod_categoria INT,
    nome VARCHAR(45) NOT NULL,
    CONSTRAINT pk_categoria PRIMARY KEY (cod_categoria)
);

CREATE TABLE biblioteca.departamento (
    cod_departamento VARCHAR(10),
    nome VARCHAR(30) NOT NULL,
    CONSTRAINT pk_departamento PRIMARY KEY (cod_departamento)
);

CREATE TABLE biblioteca.equipamentos (
    cod_equipamento INT,
    dt_aquisicao DATE NOT NULL,
    tipo VARCHAR(30) DEFAULT 'Desconhecido',
    CONSTRAINT pk_equipamentos PRIMARY KEY (cod_equipamento)
);

CREATE TABLE biblioteca.usuario (
    login VARCHAR(30),
    senha VARCHAR(45) NOT NULL,
  	cpf BIGINT UNIQUE,
    cod_usuario cod_usuario_domain NOT NULL,
    primeiro_nome VARCHAR(20) NOT NULL,
    sobrenome VARCHAR(40) NOT NULL,
    contato VARCHAR(40) NOT NULL,
    CONSTRAINT pk_usuario PRIMARY KEY (login),
    CONSTRAINT fk_usuario_contato
    FOREIGN KEY (contato)
    REFERENCES biblioteca.contato (email)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.funcionarios (
    id_funcionario INT,
    usuario_login VARCHAR(30) NOT NULL,
    cargo VARCHAR(40) NOT NULL,
    salario FLOAT NOT NULL CHECK (salario > 0),
    CONSTRAINT pk_funcionarios PRIMARY KEY (id_funcionario),
    CONSTRAINT fk_funcionarios_usuario
    FOREIGN KEY (usuario_login)
    REFERENCES biblioteca.usuario (login)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.cliente (
    usuario_login VARCHAR(30) NOT NULL UNIQUE,
    id_cliente INT,
    CONSTRAINT pk_cliente PRIMARY KEY (id_cliente),
    CONSTRAINT fk_cliente_usuario
    FOREIGN KEY (usuario_login)
    REFERENCES biblioteca.usuario (login)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.livro (
    ISBN INT,
    titulo VARCHAR(50) NOT NULL,
    ano_publi DATE NOT NULL,
    descricao VARCHAR(1000) NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade >= 0),
    edicao INT NOT NULL CHECK (edicao >= 1),
    referencias VARCHAR(500),
    idioma VARCHAR(30) NOT NULL,
    tipo_material VARCHAR(30) NOT NULL,
    secao_cod_secao VARCHAR(30) NOT NULL,
    CONSTRAINT pk_livro PRIMARY KEY (ISBN),
    CONSTRAINT fk_livro_secao
    FOREIGN KEY (secao_cod_secao)
    REFERENCES biblioteca.secao (cod_secao)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.exemplar(
    cod_ex VARCHAR(30) NOT NULL UNIQUE,
    livro_ISBN INT NOT NULL,
	status status_dom NOT NULL,
    disponibilidade VARCHAR(3) NOT NULL,
    CONSTRAINT pk_exemplar PRIMARY KEY (cod_ex, livro_ISBN),
    CONSTRAINT fk_exemplar_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.emprestimo(
    cod_emprestimo INT NOT NULL UNIQUE,
	status status_dom NOT NULL,
    dt_emprestimo DATE NOT NULL,
    dt_devolucao DATE NOT NULL,
    exemplar_codigo_ex VARCHAR(30) NOT NULL,
    exemplar_livro_ISBN INT NOT NULL,
    funcionarios_id_funcionario INT NOT NULL,
    cliente_usuario_login VARCHAR(30) NOT NULL,
    PRIMARY KEY (cod_emprestimo, exemplar_codigo_ex, exemplar_livro_ISBN),
    CONSTRAINT fk_emprestimo_exemplar
    FOREIGN KEY (exemplar_codigo_ex , exemplar_livro_ISBN)
    REFERENCES biblioteca.exemplar (cod_ex , livro_ISBN)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT fk_emprestimo_funcionarios
    FOREIGN KEY (funcionarios_id_funcionario)
    REFERENCES biblioteca.funcionarios (id_funcionario)
    ON DELETE SET NULL
    ON UPDATE CASCADE, 
  	CONSTRAINT fk_emprestimo_cliente
  	FOREIGN KEY (cliente_usuario_login)
 	REFERENCES biblioteca.cliente (usuario_login)
 	ON DELETE CASCADE
 	ON UPDATE CASCADE
);

CREATE TABLE biblioteca.reserva (
    cod_reserva INT,
    dt_reserva DATE NOT NULL,
	status status_dom NOT NULL DEFAULT 'Pendente',
    emprestimo_cod_emprestimo INT,
  	livro VARCHAR(30) NOT NULL,
    CONSTRAINT pk_reserva PRIMARY KEY (cod_reserva),
  	CONSTRAINT fk_exemplar 
  	FOREIGN KEY (livro)
  	REFERENCES biblioteca.exemplar (cod_ex)
  	ON DELETE CASCADE
    ON UPDATE CASCADE,
  	CONSTRAINT fk_emprestimo
  	FOREIGN KEY (emprestimo_cod_emprestimo)
  	REFERENCES biblioteca.emprestimo (cod_emprestimo)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.multa (
    cod_multa INT NOT NULL UNIQUE,
    status status_dom NOT NULL,
    descricao VARCHAR(50) NOT NULL,
    valor FLOAT NOT NULL  CHECK (valor > 0),
    emprestimo_cod_emprestimo INT NOT NULL,
    CONSTRAINT pk_multa PRIMARY KEY (cod_multa, emprestimo_cod_emprestimo),
	CONSTRAINT fk_multa_emprestimo
	FOREIGN KEY (emprestimo_cod_emprestimo)
	REFERENCES biblioteca.emprestimo (cod_emprestimo)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE biblioteca.fornecedor (
    cnpj VARCHAR(14),
    nome VARCHAR(45) NOT NULL,
    contato VARCHAR(40) NOT NULL,
 	status status_dom NOT NULL,
    prazo INT NOT NULL,
    CONSTRAINT pk_fornecedor PRIMARY KEY (cnpj),
    CONSTRAINT fk_fornecedor_contato
    FOREIGN KEY (contato)
    REFERENCES biblioteca.contato (email)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

CREATE TABLE biblioteca.editora (
	cnpj VARCHAR(14),
	nome VARCHAR(45) NOT NULL,
	contato VARCHAR(40) NOT NULL,
	PRIMARY KEY (cnpj),
	CONSTRAINT fk_editora_contato
	FOREIGN KEY (contato)
	REFERENCES biblioteca.contato (email)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

CREATE TABLE biblioteca.autor (
	cod_autor INT,
	nacionalidade VARCHAR(45) NULL,
	nome VARCHAR(50) NOT NULL,
	biografia VARCHAR(1000) NULL,
	contato VARCHAR(40) NOT NULL,
	CONSTRAINT pk_autor PRIMARY KEY (cod_autor),
	CONSTRAINT fk_autor_contato
	FOREIGN KEY (contato)
	REFERENCES biblioteca.contato (email)
	ON DELETE SET NULL
	ON UPDATE CASCADE
);

CREATE TABLE biblioteca.fornecedor_has_livro (
    fornecedor_cnpj VARCHAR(14) NOT NULL,
    livro_ISBN INT NOT NULL UNIQUE,
    historico_vendas VARCHAR(45) NULL,
    CONSTRAINT pk_fornecedor_livro PRIMARY KEY (fornecedor_cnpj, livro_ISBN),
    CONSTRAINT fk_fornecedor_has_livro_fornecedor
    FOREIGN KEY (fornecedor_cnpj)
    REFERENCES biblioteca.fornecedor (cnpj)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
    CONSTRAINT fk_fornecedor_has_livro_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.genero_has_livro (
    genero_cod_genero INT NOT NULL,
    livro_ISBN INT NOT NULL,
    CONSTRAINT pk_genero_livro PRIMARY KEY (genero_cod_genero, livro_ISBN),
    CONSTRAINT fk_genero_has_livro_genero
    FOREIGN KEY (genero_cod_genero)
    REFERENCES biblioteca.genero (cod_genero)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
    CONSTRAINT fk_genero_has_livro_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE SET NULL
    ON UPDATE CASCADE
  );

CREATE TABLE biblioteca.editora_has_livro (
    editora_cnpj VARCHAR(14) NOT NULL,
    livro_ISBN INT NOT NULL,
    CONSTRAINT pk_editora_livro PRIMARY KEY (editora_cnpj, livro_ISBN),
    CONSTRAINT fk_editora_has_livro_editora
    FOREIGN KEY (editora_cnpj)
    REFERENCES biblioteca.editora (cnpj)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
    CONSTRAINT fk_editora_has_livro_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.autor_has_livro (
    autor_cod_autor INT NOT NULL,
    livro_ISBN INT NOT NULL,
    CONSTRAINT pk_autor_livro PRIMARY KEY (autor_cod_autor, livro_ISBN),
    CONSTRAINT fk_autor_has_livro_autor
    FOREIGN KEY (autor_cod_autor)
    REFERENCES biblioteca.autor (cod_autor)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    CONSTRAINT fk_autor_has_livro_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE NO ACTION
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.livro_has_categoria (
    livro_ISBN INT NOT NULL,
    categoria_cod_categoria INT NOT NULL,
    CONSTRAINT pk_categoria_livro 
  	PRIMARY KEY (livro_ISBN, categoria_cod_categoria),
    CONSTRAINT fk_livro_has_categoria_livro
    FOREIGN KEY (livro_ISBN)
    REFERENCES biblioteca.livro (ISBN)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
    CONSTRAINT fk_livro_has_categoria_categoria
    FOREIGN KEY (categoria_cod_categoria)
    REFERENCES biblioteca.categoria (cod_categoria)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.funcionarios_has_departamento (
	login_funcionario VARCHAR(30),
    departamento_cod_departamento VARCHAR(10) NOT NULL,
    dt_admissao DATE NOT NULL,
    dt_demissao DATE NULL,
    CONSTRAINT pk_departamento_funcionario
  	PRIMARY KEY (login_funcionario, departamento_cod_departamento),
    CONSTRAINT fk_funcionarios_has_departamento_funcionarios
    FOREIGN KEY (login_funcionario)
    REFERENCES biblioteca.usuario(login)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT fk_funcionarios_has_departamento_departamento
    FOREIGN KEY (departamento_cod_departamento)
    REFERENCES biblioteca.departamento (cod_departamento)
    ON DELETE SET NULL
    ON UPDATE CASCADE
);

CREATE TABLE biblioteca.funcionarios_has_equipamentos (
    funcionarios_id_funcionario INT NOT NULL,
    equipamentos_cod_equipamento INT NOT NULL,
    dt_utilização DATE NOT NULL,
    status VARCHAR(45) NOT NULL,
    CONSTRAINT pk_equipamento_funcionario
  	PRIMARY KEY (funcionarios_id_funcionario, equipamentos_cod_equipamento),
    CONSTRAINT fk_funcionarios_has_equipamentos_funcionarios
    FOREIGN KEY (funcionarios_id_funcionario)
    REFERENCES biblioteca.funcionarios (id_funcionario)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
    CONSTRAINT fk_funcionarios_has_equipamentos_equipamentos
    FOREIGN KEY (equipamentos_cod_equipamento)
    REFERENCES biblioteca.equipamentos (cod_equipamento)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);