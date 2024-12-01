import requests
import matplotlib.pyplot as plt
import numpy as np
import pwinput

url = "http://localhost:3000/camisetas"
url_login = "http://localhost:3000/login"

usuario_id = ""
token = ""


def login():
    titulo("Login do Usuário")

    email = input("E-mail...: ")
    senha = pwinput.pwinput(prompt='Senha....: ')

    response = requests.post(url_login, json={
        "email": email,
        "senha": senha
    })

    if response.status_code == 200:
        resposta = response.json()
        global usuario_id
        global token
        usuario_id = resposta['id']
        token = resposta['token']
        print(f"Ok! Bem-vindo {resposta['nome']}")
    else:
        print("Erro... Não foi possível realizar login no sistema")


def inclusao():
    titulo("Inclusão de Camisetas", "=")

    if token == "":
        print("Erro... Você precisa fazer login para incluir camisetas")
        return

    modelo = input("Modelo......: ")
    marca = input("Marca.......: ")
    preco = float(input("Preço R$....: "))

    response = requests.post(url,
                             headers={"Authorization": f"Bearer {token}"},
                             json={
                                 "modelo": modelo,
                                 "marca": marca,
                                 "preco": preco,
                                 "usuarioId": usuario_id
                             })

    if response.status_code == 201:
        camiseta = response.json()
        print(f"Ok! Camiseta cadastrada com código: {camiseta['id']}")
    else:
        print("Erro... Não foi possível incluir a camiseta")


def listagem():
    titulo("Listagem das Camisetas Cadastradas", "=")

    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    camisetas = response.json()

    print("Cód. Modelo.............: Marca.........: Preço R$: Quantidade:")
    print("-------------------------------------------------------------")

    for camiseta in camisetas:
        print(
            f"{camiseta['id']:4d} {camiseta['modelo']:20s} {camiseta['marca']:15s} {float(camiseta['preco']):9.2f}"
        )


def grafico_media_preco():
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    camisetas = response.json()
    modelos = list(set([x['modelo'] for x in camisetas]))
    media_precos = [0] * len(modelos)

    for i, modelo in enumerate(modelos):
        precos = [float(x['preco']) for x in camisetas if x['modelo'] == modelo]
        media_precos[i] = sum(precos) / len(precos) if len(precos) > 0 else 0

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(modelos, media_precos)
    ax.set_title("Média de Preços por Modelo")
    ax.set_xlabel("Modelo")
    ax.set_ylabel("Média de Preço (R$)")

    plt.show()


def grafico_quantidade_marca():
    response = requests.get(url)

    if response.status_code != 200:
        print("Erro... Não foi possível acessar a API")
        return

    camisetas = response.json()

    marcas = list(set([x['marca'] for x in camisetas if 'marca' in x]))

    quantidades = [0] * len(marcas)

    for i, marca in enumerate(marcas):
        quantidades[i] = sum([1 for x in camisetas if x.get('marca') == marca])

    if all(q == 0 for q in quantidades):
        print("Não foi possível calcular a quantidade de camisetas por marca.")
        return

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(marcas, quantidades, marker='o')
    ax.set_title("Quantidade de Itens por Marca")
    ax.set_xlabel("Marca")
    ax.set_ylabel("Quantidade de Itens")

    plt.show()


def deletar():
    titulo("Deletar Camiseta", "=")

    if token == "":
        print("Erro... Você precisa fazer login para deletar camisetas")
        return

    codigo = int(input("Código da Camiseta: "))

    response = requests.delete(f"{url}/{codigo}",
                               headers={"Authorization": f"Bearer {token}"})

    if response.status_code == 200:
        print("Ok! Camiseta deletada com sucesso")
    else:
        print("Erro... Não foi possível deletar a camiseta")

def titulo(texto, traco="-"):
    print()
    print(texto)
    print(traco*40)


while True:
    titulo("Cadastro de Camisetas")
    print("1. Login do Usuário")
    print("2. Inclusão de Camisetas")
    print("3. Listagem de Camisetas")
    print("4. Gráfico: Média de Preços por Modelo (Barras)")
    print("5. Gráfico: Quantidade de Camisetas por Marca (Linha)")
    print("6. Deletar Camiseta")
    print("7. Finalizar")
    opcao = int(input("Opção: "))
    if opcao == 1:
        login()
    elif opcao == 2:
        inclusao()
    elif opcao == 3:
        listagem()
    elif opcao == 4:
        grafico_media_preco()
    elif opcao == 5:
        grafico_quantidade_marca()
    elif opcao == 6:
        deletar()
    else:
        break
