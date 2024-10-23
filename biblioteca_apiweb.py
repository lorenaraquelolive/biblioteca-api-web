from flask import Flask, request, jsonify
import psycopg2

class BancoDeDadosPostgres:
    def __init__(self):
        # Configurações de conexão com o banco de dados PostgreSQL
        try:
            self.conexao = psycopg2.connect(
                host='bd-atividade.cev0emweyiep.us-east-1.rds.amazonaws.com',
                user='postgres',  # Usuário do PostgreSQL
                password='postgres',  # Senha do PostgreSQL
                database='Biblioteca'  # Nome do banco de dados
            )
            self.cursor = self.conexao.cursor()
            print("Conexão bem-sucedida!")
        except psycopg2.Error as err:
            print(f"Erro ao conectar ao banco de dados: {err}")

    
    def delete_contato(self, email):
        try:
            sql = "DELETE FROM biblioteca.contato WHERE email = %s"
            self.cursor.execute(sql, (email,))
            self.conexao.commit()
            return True
        except psycopg2.Error as err:
            print(f"Erro ao deletar contato: {err}")
            return False

    def delete_usuario(self, login):
        try:
            sql = "DELETE FROM biblioteca.usuario WHERE login = %s"
            self.cursor.execute(sql, (login,))
            self.conexao.commit()
            return True
        except psycopg2.Error as err:
            print(f"Erro ao deletar usuário: {err}")
            return False


    ###FUNCIONÁRIO###
    # create
    def inserir_funcionario(self, email, telefone, cep, rua, bairro, cidade, estado, pais,  # contato
                            login, senha, cpf, cod_usuario, primeiro_nome, sobrenome,  # usuário
                            id_funcionario, cargo, salario):  # funcionario
        try:
            sql_contato = 'INSERT INTO biblioteca.contato (email, telefone, cep, rua, bairro, cidade, estado, pais) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
            valores_contato = (email, telefone, cep, rua, bairro, cidade, estado, pais)
            self.cursor.execute(sql_contato, valores_contato)
            self.conexao.commit()

            sql_usuario = 'INSERT INTO biblioteca.usuario (login, senha, cpf, cod_usuario, primeiro_nome, sobrenome, contato) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            valores_usuario = (login, senha, cpf, cod_usuario, primeiro_nome, sobrenome, email)
            self.cursor.execute(sql_usuario, valores_usuario)
            self.conexao.commit()

            sql_funcionario = 'INSERT INTO biblioteca.funcionarios (id_funcionario, usuario_login, cargo, salario) VALUES (%s, %s, %s, %s)'
            valores_funcionario = (id_funcionario, login, cargo, salario)
            self.cursor.execute(sql_funcionario, valores_funcionario)
            self.conexao.commit()

            print("Funcionário inserido com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao inserir funcionário: {err}")
            return False
        
        #inserir funcionário com usuário já existente
    def inserir_funcionario_existente(self, id_funcionario, login, cargo, salario):
        try:
            sql = 'INSERT INTO biblioteca.funcionarios (id_funcionario, usuario_login, cargo, salario) VALUES (%s, %s, %s, %s)'
            valores_funcionario = (id_funcionario, login, cargo, salario)
            self.cursor.execute(sql, valores_funcionario)
            self.conexao.commit()
            print("Funcionário inserido com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao inserir funcionário: {err}")
            return False

    # read tabela
    def listar_funcionarios(self):
        try:
            sql = 'SELECT * FROM biblioteca.funcionarios'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            print(f"Erro ao consultar funcionários: {err}")
            return None

    # read linha
    def consultar_funcionario(self, id_funcionario):
        try:
            sql = 'SELECT * FROM biblioteca.funcionarios WHERE id_funcionario = %s'
            self.cursor.execute(sql, (id_funcionario,))
            return self.cursor.fetchone()
        except psycopg2.Error as err:
            print(f"Erro ao consultar funcionário: {err}")
            return None
        
    # update
    def update_funcionario(self, id_funcionario, cargo, salario):
        try:
            sql = 'UPDATE biblioteca.funcionarios SET salario = %s, cargo = %s WHERE id_funcionario = %s'
            valores = (id_funcionario, cargo, salario)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Funcionário alterado com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao atualizar funcionário: {err}")
            return False

    # update separado
    def update_funcionario_cargo(self, id_funcionario, cargo):
        try:
            sql = 'UPDATE biblioteca.funcionarios SET cargo = %s WHERE id_funcionario = %s'
            valores = (cargo, id_funcionario)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Cargo alterado com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao alterar: {err}")
            return False

    def update_funcionario_salario(self, salario, id_funcionario):
        try:
            sql = 'UPDATE biblioteca.funcionarios SET salario = %s WHERE id_funcionario = %s'
            valores = (salario, id_funcionario)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Salário alterado com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao alterar: {err}")
            return False

    # delete
    def delete_funcionario(self, id_funcionario):
        try:
            sql = 'DELETE FROM biblioteca.funcionarios WHERE id_funcionario = %s'
            self.cursor.execute(sql, (id_funcionario,))
            self.conexao.commit()
            print("Funcionário removido com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao deletar funcionário: {err}")
            return False

    ###DEPARTAMENTO###
    # create
    def inserir_departamento(self, cod_departamento, nome):
        try:
            sql = 'INSERT INTO biblioteca.departamento (cod_departamento, nome) VALUES (%s, %s)'
            valores = (cod_departamento, nome)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Departamento inserido com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao inserir departamento: {err}")
            return False

    # read
    def listar_departamentos(self):
        try:
            sql = 'SELECT * FROM biblioteca.departamento'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            print(f"Erro ao consultar departamentos: {err}")
            return None

    def consultar_departamento(self, cod_departamento):
        try:
            sql = 'SELECT * FROM biblioteca.departamento WHERE cod_departamento = %s'
            self.cursor.execute(sql, (cod_departamento,))
            return self.cursor.fetchone()
        except psycopg2.Error as err:
            print(f"Erro ao consultar departamento: {err}")
            return None

    # update
    def update_departamento(self, cod_departamento, nome):
        try:
            sql = 'UPDATE biblioteca.departamento SET nome = %s WHERE cod_departamento = %s'
            valores = (nome, cod_departamento)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Nome de departamento alterado com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao atualizar departamento: {err}")
            return False

    # delete
    def delete_departamento(self, cod_departamento):
        try:
            sql = 'DELETE FROM biblioteca.departamento WHERE cod_departamento = %s'
            self.cursor.execute(sql, (cod_departamento,))
            self.conexao.commit()
            sql = 'DELETE FROM biblioteca.funcionarios_has_departamento WHERE departamento_cod_departamento = %s'
            self.cursor.execute(sql, (cod_departamento,))
            self.conexao.commit()
            print("Departamento removido com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao deletar departamento: {err}")
            return False

    ###funcionarios_has_departamento###
    # create
    def inserir_funcionario_em_departamento(self, login_funcionario, cod_departamento, dt_admissao):
        try:
            sql = 'INSERT INTO biblioteca.funcionarios_has_departamento (login_funcionario, departamento_cod_departamento, dt_admissao) VALUES (%s, %s, %s)'
            valores = (login_funcionario, cod_departamento, dt_admissao)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Funcionário adicionado ao departamento com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao inserir funcionário em departamento: {err}")
            return False

    # read
    def consultar_funcionarios_has_departamento(self):
        try:
            sql = 'SELECT * FROM biblioteca.funcionarios_has_departamento'
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            print(f"Erro ao consultar funcionários em departamentos: {err}")
            return None

    # consultar todos os funcionários daquele departamento
    def consultar_funcionarios_em_departamento(self, cod_departamento):
        try:
            sql = 'SELECT login_funcionario FROM biblioteca.funcionarios_has_departamento WHERE departamento_cod_departamento = %s'
            self.cursor.execute(sql, (cod_departamento,))
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            print(f"Erro ao consultar funcionários no departamento: {err}")
            return None

    # consultar o departamento do funcionário
    def consultar_departamento_de_funcionario(self, login_funcionario):
        try:
            sql = 'SELECT * FROM biblioteca.funcionarios_has_departamento WHERE login_funcionario = %s'
            self.cursor.execute(sql, (login_funcionario,))
            return self.cursor.fetchall()
        except psycopg2.Error as err:
            print(f"Erro ao consultar: {err}")
            return None

    # update
    # alterar departamento do funcionário
    def update_funcionario_departamento(self, login_funcionario, cod_departamento):
        try:
            sql = 'UPDATE biblioteca.funcionarios_has_departamento SET departamento_cod_departamento = %s WHERE login_funcionario = %s'
            valores = (cod_departamento, login_funcionario)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Funcionário transferido de departamento com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao atualizar funcionário em departamento: {err}")
            return False
        
    #alterar data da demissão
    def update_demissao(self, login_funcionario, dt_demissao):
        try:
            sql = 'UPDATE biblioteca.funcionarios_has_departamento SET dt_demissao = %s WHERE login_funcionario = %s'
            valores = (dt_demissao, login_funcionario)
            self.cursor.execute(sql, valores)
            self.conexao.commit()
            print("Data de demissão alterada com sucesso")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao alterar: {err}")
            return False

    # delete
    def deletar_funcionario_em_departamento(self, login_funcionario):
        try:
            sql = 'DELETE FROM biblioteca.funcionarios_has_departamento WHERE login_funcionario = %s'
            self.cursor.execute(sql, login_funcionario)
            self.conexao.commit()
            print("Funcionário removido do departamento com sucesso.")
            return True
        except psycopg2.Error as err:
            print(f"Erro ao deletar funcionário em departamento: {err}")
            return False

# Inicialização da API Flask
app = Flask(__name__)

# Criar uma instância de BancoDeDadosPostgres
bd = BancoDeDadosPostgres()

### Rotas da API ###
# Rota raiz
@app.route('/', methods=['GET'])
def raiz():
    return jsonify({'mensagem': 'Bem-vindo a API da Biblioteca!'}), 200

# Rota para deletar um contato por email
@app.route('/contato/<email>', methods=['DELETE'])
def deletar_contato(email):
    sucesso = bd.delete_contato (email)
    if sucesso:
        return jsonify({"mensagem": "Contato deletado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Erro ao deletar contato"}), 500

# Rota para deletar um usuário por login
@app.route('/usuario/<login>', methods=['DELETE'])
def deletar_usuario(login):
    sucesso = bd.delete_usuario(login)
    if sucesso:
        return jsonify({"mensagem": "Usuario deletado com sucesso"}), 200
    else:
        return jsonify({"mensagem": "Erro ao deletar usuário"}), 500

###FUNCIONÁRIO###
# create
@app.route('/funcionario', methods=['POST'])
def criar_funcionario():
    dados = request.json
    sucesso = bd.inserir_funcionario(dados['email'], dados['telefone'], dados['cep'], dados['rua'], dados['bairro'], dados['cidade'], dados['estado'], dados['pais'], # contato
                                     dados['login'], dados['senha'], dados['cpf'], dados['cod_usuario'], dados['primeiro_nome'], dados['sobrenome'],  # usuario
                                     dados['salario'], dados['cargo'], dados['id_funcionario'])  # funcionario
    if sucesso:
        return jsonify({'mensagem': 'Funcionario criado com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Erro ao criar funcionario'}), 400

# Rota para inserir um funcionário com usuário já existente
@app.route('/funcionario/existente', methods=['POST'])
def criar_funcionario_existente():
    dados = request.json
    sucesso = bd.inserir_funcionario_existente(
        dados['salario'],
        dados['cargo'],
        dados['id_funcionario'],
        dados['login']
    )
    
    if sucesso:
        return jsonify({'mensagem': 'Funcionario inserido com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Erro ao inserir funcionario, login do usuário'}), 400

# read tabela
@app.route('/funcionarios', methods=['GET'])
def listar_funcionarios():
    funcionarios = bd.listar_funcionarios()
    if funcionarios:
        return jsonify(funcionarios), 200
    else:
        return jsonify({'mensagem': 'Nenhum funcionario encontrado'}), 404

# read linha
@app.route('/funcionario/<int:id_funcionario>', methods=['GET'])
def consultar_funcionario(id_funcionario):
    funcionario = bd.consultar_funcionario(id_funcionario)
    if funcionario:
        return jsonify(funcionario), 200
    else:
        return jsonify({'mensagem': 'Funcionario nao encontrado'}), 404

# update
@app.route('/funcionario/<int:id_funcionario>', methods=['PUT'])
def update_funcionario(id_funcionario):
    dados = request.json
    sucesso = bd.update_funcionario(dados['salario'], dados['cargo'], id_funcionario)
    if sucesso:
        return jsonify({'mensagem': 'Funcionario atualizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao atualizar funcionário'}), 400

# update salário ou cargo
@app.route('/funcionario-salario/<int:id_funcionario>', methods=['PUT'])
def atualizar_funcionario_salario(id_funcionario):
    dados = request.json
    sucesso = bd.update_funcionario_salario(dados['salario'], id_funcionario)
    if sucesso:
        return jsonify({'mensagem': 'Salario atualizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao atualizar salário'}), 400

@app.route('/funcionario-cargo/<int:id_funcionario>', methods=['PUT'])
def atualizar_funcionario_cargo(id_funcionario):
    dados = request.json
    sucesso = bd.update_funcionario_cargo(dados['cargo'], id_funcionario)
    if sucesso:
        return jsonify({'mensagem': 'Cargo atualizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao atualizar cargo'}), 400

# delete
@app.route('/funcionario/<int:id_funcionario>', methods=['DELETE'])
def deletar_funcionario(id_funcionario):
    sucesso = bd.delete_funcionario(id_funcionario)
    if sucesso:
        return jsonify({'mensagem': 'Funcionario deletado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao deletar funcionario'}), 400

###DEPARTAMENTO###
# create
@app.route('/departamento', methods=['POST'])
def criar_departamento():
    dados = request.json
    sucesso = bd.inserir_departamento(dados['cod_departamento'], dados['nome'])
    if sucesso:
        return jsonify({'mensagem': 'Departamento criado com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Erro ao criar departamento'}), 400

# read tabela
@app.route('/departamentos', methods=['GET'])
def listar_departamentos():
    departamentos = bd.listar_departamentos()
    if departamentos:
        return jsonify(departamentos), 200
    else:
        return jsonify({'mensagem': 'Nenhum departamento encontrado'}), 404

# read linha
@app.route('/departamento/<cod_departamento>', methods=['GET'])
def consultar_departamento(cod_departamento):
    departamento = bd.consultar_departamento(cod_departamento)
    if departamento:
        return jsonify(departamento), 200
    else:
        return jsonify({'mensagem': 'Departamento nao encontrado'}), 404

# update
@app.route('/departamento/<cod_departamento>', methods=['PUT'])
def atualizar_departamento(cod_departamento):
    dados = request.json
    sucesso = bd.update_departamento(cod_departamento, dados['nome'])
    if sucesso:
        return jsonify({'mensagem': 'Departamento atualizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao atualizar departamento'}), 400

# delete
@app.route('/departamento/<cod_departamento>', methods=['DELETE'])
def deletar_departamento(cod_departamento):
    sucesso = bd.delete_departamento(cod_departamento)
    if sucesso:
        return jsonify({'mensagem': 'Departamento deletado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao deletar departamento'}), 400

###FUNCIONÁRIO_HAS_DEPARTAMENTO###
# create
@app.route('/funcionario-departamento', methods=['POST'])
def criar_funcionario_em_departamento():
    dados = request.json
    sucesso = bd.inserir_funcionario_em_departamento(dados['login_funcionario'], dados['cod_departamento'], dados['dt_admissao'])
    if sucesso:
        return jsonify({'mensagem': 'Funcionario adicionado ao departamento com sucesso'}), 201
    else:
        return jsonify({'mensagem': 'Erro ao adicionar funcionario ao departamento'}), 400

# read tabela
@app.route('/funcionarios-departamentos', methods=['GET'])
def listar_funcionarios_em_departamentos():
    funcionarios_departamentos = bd.consultar_funcionarios_has_departamento()
    if funcionarios_departamentos:
        return jsonify(funcionarios_departamentos), 200
    else:
        return jsonify({'mensagem': 'Nenhum registro encontrado'}), 404

# read funcionários do departamento
@app.route('/funcionario-departamento/<cod_departamento>', methods=['GET'])
def consultar_funcionarios_no_departamento(cod_departamento):
    funcionarios = bd.consultar_funcionarios_em_departamento(cod_departamento)
    if funcionarios:
        return jsonify(funcionarios), 200
    else:
        return jsonify({'mensagem': 'Nenhum funcionario encontrado para o departamento'}), 404

# read departamento do funcionário
@app.route('/departamento-funcionario/<login_funcionario>', methods=['GET'])
def consultar_departamento_de_funcionario(login_funcionario):
    departamento = bd.consultar_departamento_de_funcionario(login_funcionario)
    if departamento:
        return jsonify(departamento), 200
    else:
        return jsonify({'mensagem': 'Funcionario não está em nenhum departamento'}), 404

# update
@app.route('/funcionario-departamento/<login_funcionario>', methods=['PUT'])
def atualizar_funcionario_departamento(login_funcionario):
    dados = request.json
    sucesso = bd.update_funcionario_departamento(login_funcionario, dados['cod_departamento'])
    if sucesso:
        return jsonify({'mensagem': 'Departamento do funcionario atualizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao atualizar departamento do funcionario'}), 400

#alterar data da demissão
@app.route('/funcionario-demissao/<login_funcionario>', methods=['PUT'])
def alterar_demissao(login_funcionario):
    dados = request.json
    sucesso = bd.update_demissao(login_funcionario, dados['dt_demissao'])
    if sucesso:
        return jsonify({'mensagem': 'Data da demissão alterada com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao alterar a data da demissão'}), 400

# delete
@app.route('/funcionario-departamento/<login_funcionario>', methods=['DELETE'])
def deletar_funcionario_em_departamento(login_funcionario):
    sucesso = bd.deletar_funcionario_em_departamento(login_funcionario)
    if sucesso:
        return jsonify({'mensagem': 'Funcionario removido do departamento com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Erro ao remover funcionario do departamento'}), 400

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)