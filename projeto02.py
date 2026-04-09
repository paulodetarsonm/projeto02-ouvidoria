import mysql.connector

# ========== FUNÇÕES DO BANCO DE DADOS ==========

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

def inicializarTabela(connection):
    try:
        cursor = connection.cursor()
        sql = """
        CREATE TABLE IF NOT EXISTS reclamacoes (
            codigo INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            descricao TEXT NOT NULL
        )
        """
        cursor.execute(sql)
        connection.commit()
        print("Tabela verificada/criada com sucesso!")
    except mysql.connector.Error as err:
        print(f"Erro ao criar tabela: {err}")
    finally:
        cursor.close()

def encerrarConexao(connection):
    if connection:
        connection.close()

def insertNoBancoDados(connection, sql, dados):
    try:
        cursor = connection.cursor(prepared=True)
        cursor.execute(sql, dados)
        connection.commit()
        id = cursor.lastrowid
    except mysql.connector.Error as err:
        print(f"Erro ao inserir no banco de dados: {err}")
        connection.rollback()
        return None
    finally:
        cursor.close()
    return id

def listarBancoDados(connection, sql, params=None):
    try:
        cursor = connection.cursor(prepared=True)
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

def atualizarBancoDados(connection, sql, dados):
    try:
        cursor = connection.cursor(prepared=True)
        cursor.execute(sql, dados)
        connection.commit()
        linhasAfetadas = cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao atualizar o banco de dados: {err}")
        connection.rollback()
        return 0
    finally:
        cursor.close()
    return linhasAfetadas

def excluirBancoDados(connection, sql, dados):
    try:
        cursor = connection.cursor(prepared=True)
        cursor.execute(sql, dados)
        connection.commit()
        linhasAfetadas = cursor.rowcount
    except mysql.connector.Error as err:
        print(f"Erro ao excluir do banco de dados: {err}")
        connection.rollback()
        return 0
    finally:
        cursor.close()
    return linhasAfetadas



# ========== FUNÇÕES DO SISTEMA DE OUVIDORIA ==========

def registrar_reclamacao(connection):
    nome = input("Digite seu nome: ")
    descricao = input("Digite a reclamação: ")

    sql = """
        INSERT INTO reclamacoes (nome, descricao)
        VALUES (%s, %s)
    """

    codigo = insertNoBancoDados(connection, sql, (nome, descricao))

    if codigo:
        print("Reclamação registrada com sucesso!")
        print(f"O código da sua reclamação é: {codigo}")
    else:
        print("Erro ao registrar reclamação.")


def listar_reclamacoes(connection):
    sql = "SELECT codigo, nome, descricao FROM reclamacoes"

    reclamacoes = listarBancoDados(connection, sql)

    if len(reclamacoes) == 0:
        print("Nenhuma reclamação cadastrada.")
    else:
        for r in reclamacoes:
            print("\nCódigo:", r[0])
            print("Nome:", r[1])
            print("Descrição:", r[2])


def pesquisar_reclamacao(connection):
    busca = int(input("Digite o código da reclamação: "))

    sql = "SELECT nome, descricao FROM reclamacoes WHERE codigo = %s"
    resultado = listarBancoDados(connection, sql, (busca,))

    if resultado:
        print("Nome:", resultado[0][0])
        print("Descrição:", resultado[0][1])
    else:
        print("Reclamação não encontrada.")


def atualizar_reclamacao(connection):
    busca = int(input("Digite o código da reclamação: "))

    nova = input("Digite a nova descrição: ")

    sql = "UPDATE reclamacoes SET descricao = %s WHERE codigo = %s"

    linhas = atualizarBancoDados(connection, sql, (nova, busca))

    if linhas > 0:
        print("Reclamação atualizada!")
    else:
        print("Reclamação não encontrada.")


def remover_reclamacao(connection):
    busca = int(input("Digite o código da reclamação: "))

    sql = "DELETE FROM reclamacoes WHERE codigo = %s"

    linhas = excluirBancoDados(connection, sql, (busca,))

    if linhas > 0:
        print("Reclamação removida!")
    else:
        print("Reclamação não encontrada.")


def quantidade_reclamacoes(connection):
    sql = "SELECT COUNT(*) FROM reclamacoes"
    total = listarBancoDados(connection, sql)

    print("Total de reclamações:", total[0][0])



# ========== MENU PRINCIPAL ==========

def menu():
    connection = criarConexao("localhost", "root", "Paulofaro@27", "ouvidoria")

    if connection is None:
        print("Não foi possível iniciar o sistema.")
        return

    inicializarTabela(connection)

    opcao = 0
    while opcao != 7:

        print("\n--- SISTEMA DE OUVIDORIA ---")
        print("1 - Registrar reclamação")
        print("2 - Listar reclamações")
        print("3 - Pesquisar reclamação")
        print("4 - Atualizar reclamação")
        print("5 - Remover reclamação")
        print("6 - Quantidade de reclamações")
        print("7 - Sair")

        opcao = int(input("Escolha uma opção: "))

        if opcao == 1:
            registrar_reclamacao(connection)

        elif opcao == 2:
            listar_reclamacoes(connection)

        elif opcao == 3:
            pesquisar_reclamacao(connection)

        elif opcao == 4:
            atualizar_reclamacao(connection)

        elif opcao == 5:
            remover_reclamacao(connection)

        elif opcao == 6:
            quantidade_reclamacoes(connection)

        elif opcao == 7:
            print("Saindo do sistema...")

        else:
            print("Opção inválida!")

    encerrarConexao(connection)


menu()