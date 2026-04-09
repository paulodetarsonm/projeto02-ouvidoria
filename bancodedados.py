import mysql.connector

#  FUNÇÕES DO BANCO DE DADOS

def criarConexao(endereco, usuario, senha, bancodedados):
    try:
        return mysql.connector.connect(
            host=endereco,
            user=usuario,
            password=senha,
            database=bancodedados
        )
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None

def inicializarTabela(conexao):
    try:
        cursor = conexao.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS reclamacoes (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL
        )
        """
        cursor.execute(sql)
        conexao.commit()
        print("Tabela verificada/criada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar tabela: {err}")
    finally:
        cursor.close()

def encerrarConexao(conexao):
    if conexao:
        conexao.close()

def insertNoBancoDados(conexao, sql, dados):
    try:
        cursor = conexao.cursor(prepared=True)
        cursor.execute(sql, dados)
        conexao.commit()
        id = cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no banco de dados: {err}")
        conexao.rollback()
        return None
    finally:
        cursor.close()
    return id

def listarBancoDados(conexao, sql, params=None):
    try:
        cursor = conexao.cursor(prepared=True)
        if params is None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, params)
        results = cursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Erro ao listar do banco de dados: {err}")
        return []
    finally:
        cursor.close()
    return results

def atualizarBancoDados(conexao, sql, dados):
    try:
        cursor = conexao.cursor(prepared=True)
        cursor.execute(sql, dados)
        conexao.commit()
        linhasAfetadas = cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar o banco de dados: {err}")
        conexao.rollback()
        return 0
    finally:
        cursor.close()
    return linhasAfetadas

def excluirBancoDados(conexao, sql, dados):
    try:
        cursor = conexao.cursor(prepared=True)
        cursor.execute(sql, dados)
        conexao.commit()
        linhasAfetadas = cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao excluir do banco de dados: {err}")
        conexao.rollback()
        return 0
    finally:
        cursor.close()
    return linhasAfetadas

