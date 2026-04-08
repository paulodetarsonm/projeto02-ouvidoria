reclamacoes = []
codigo = 1


def registrar_reclamacao():
    global codigo

    nome = input("Digite seu nome: ")
    descricao = input("Digite a reclamação: ")

    reclamacao = {
        "codigo": codigo,
        "nome": nome,
        "descricao": descricao
    }

    reclamacoes.append(reclamacao)
    codigo += 1

    print("Reclamação registrada com sucesso!")
    print(f'O código da sua reclamação é: {reclamacao["codigo"]}')


def listar_reclamacoes():
    if len(reclamacoes) == 0:
        print("Nenhuma reclamação cadastrada.")
    else:
        for i in range(len(reclamacoes)):
            print("\nCódigo:", reclamacoes[i]["codigo"])
            print("Nome:", reclamacoes[i]["nome"])
            print("Descrição:", reclamacoes[i]["descricao"])


def pesquisar_reclamacao():
    busca = int(input("Digite o código da reclamação: "))

    for r in reclamacoes:
        if r["codigo"] == busca:
            print("Nome:", r["nome"])
            print("Descrição:", r["descricao"])
            return

    print("Reclamação não encontrada.")


def atualizar_reclamacao():
    busca = int(input("Digite o código da reclamação: "))

    for r in reclamacoes:
        if r["codigo"] == busca:
            nova = input("Digite a nova descrição: ")
            r["descricao"] = nova
            print("Reclamação atualizada!")
            return

    print("Reclamação não encontrada.")


def remover_reclamacao():
    busca = int(input("Digite o código da reclamação: "))

    for r in reclamacoes:
        if r["codigo"] == busca:
            reclamacoes.remove(r)
            print("Reclamação removida!")
            return

    print("Reclamação não encontrada.")


def quantidade_reclamacoes():
    print("Total de reclamações:", len(reclamacoes))


def menu():

    opcao = 0
    while opcao!=7:

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
            registrar_reclamacao()

        elif opcao == 2:
            listar_reclamacoes()

        elif opcao == 3:
            pesquisar_reclamacao()

        elif opcao == 4:
            atualizar_reclamacao()

        elif opcao == 5:
            remover_reclamacao()

        elif opcao == 6:
            quantidade_reclamacoes()

        elif opcao == 7:
            print("Saindo do sistema...")

        else:
            print("Opção inválida!")


menu()