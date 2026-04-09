from bancodedados import *
import os
from dotenv import load_dotenv

load_dotenv()

#  FUNÇÕES DO SISTEMA DE OUVIDORIA 

def registrar_reclamacao(conexao):
    nome = input("Digite seu nome: ")
    descricao = input("Digite a reclamação: ")

    sql = """
        INSERT INTO reclamacoes (nome, descricao)
        VALUES (%s, %s)
    """

    codigo = insertNoBancoDados(conexao, sql, (nome, descricao))

    if codigo:
        print("Reclamação registrada com sucesso!")
        print(f"O código da sua reclamação é: {codigo}")
    else:
        print("Erro ao registrar reclamação.")


def listar_reclamacoes(conexao):
    sql = "SELECT codigo, nome, descricao FROM reclamacoes"

    reclamacoes = listarBancoDados(conexao, sql)

    if len(reclamacoes) == 0:
        print("Nenhuma reclamação cadastrada.")
    else:
        for r in reclamacoes:
            print("\nCódigo:", r[0])
            print("Nome:", r[1])
            print("Descrição:", r[2])


def pesquisar_reclamacao(conexao):
    busca = int(input("Digite o código da reclamação: "))

    sql = "SELECT nome, descricao FROM reclamacoes WHERE codigo = %s"
    resultado = listarBancoDados(conexao, sql, (busca,))

    if resultado:
        print("Nome:", resultado[0][0])
        print("Descrição:", resultado[0][1])
    else:
        print("Reclamação não encontrada.")


def atualizar_reclamacao(conexao):
    busca = int(input("Digite o código da reclamação: "))

    nova = input("Digite a nova descrição: ")

    sql = "UPDATE reclamacoes SET descricao = %s WHERE codigo = %s"

    linhas = atualizarBancoDados(conexao, sql, (nova, busca))

    if linhas > 0:
        print("Reclamação atualizada!")
    else:
        print("Reclamação não encontrada.")


def remover_reclamacao(conexao):
    busca = int(input("Digite o código da reclamação: "))

    sql = "DELETE FROM reclamacoes WHERE codigo = %s"

    linhas = excluirBancoDados(conexao, sql, (busca,))

    if linhas > 0:
        print("Reclamação removida!")
    else:
        print("Reclamação não encontrada.")


def quantidade_reclamacoes(conexao):
    sql = "SELECT COUNT(*) FROM reclamacoes"
    total = listarBancoDados(conexao, sql)

    print("Total de reclamações:", total[0][0])



#  MENU PRINCIPAL 

def menu():

    host = os.getenv("DB_HOST")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    bd_name = os.getenv("DB_NAME")
    conexao = criarConexao(host, user, password, bd_name)

    if conexao is None:
        print("Não foi possível iniciar o sistema.")
        return

    inicializarTabela(conexao)

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
            registrar_reclamacao(conexao)

        elif opcao == 2:
            listar_reclamacoes(conexao)

        elif opcao == 3:
            pesquisar_reclamacao(conexao)

        elif opcao == 4:
            atualizar_reclamacao(conexao)

        elif opcao == 5:
            remover_reclamacao(conexao)

        elif opcao == 6:
            quantidade_reclamacoes(conexao)

        elif opcao == 7:
            print("Saindo do sistema...")

        else:
            print("Opção inválida!")

    encerrarConexao(conexao)


menu()