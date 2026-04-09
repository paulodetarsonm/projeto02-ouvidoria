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

