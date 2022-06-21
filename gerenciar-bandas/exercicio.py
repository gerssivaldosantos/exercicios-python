import json
import string 

path_bandas = 'bandas.json'
path_musicos = 'musicos.json'

"""

--------------------------- CheckList ----------------------------

[V] Cadastrar músicos
[X] Buscar músicos por email
[X] Buscar músicos por nome
[X] Buscar músicos por gênero músical
[X] Buscar músicos por nome
[X] Modificar músicos
[V] Montar bandas
[V] Sair

-------------- Regras dos dados de cadastro do músico --------------

* Nome (string contendo apenas letras e espaço)

* E-mail (string contendo apenas letras, underscore (_), ponto (.), 
dígitos numéricos e, obrigatoriamente, exatamente 1 arroba (@))

* Gêneros musicais (mínimo 1, usuário pode digitar quantos forem necessários)

* Instrumentos (mínimo 1, usuário pode digitar quantos forem necessários)

As entradas devem ser validadas seguindo as regras. O e-mail deve ser único: 
se ele já existe, o cadastro não deve ser concluído.

----------------- regras atualização dados músico -----------------

* Na modificação de um usuário, será feita uma busca especificamente por e-mail.

* É permitido adicionar ou remover gêneros e instrumentos. 

* Não é permitido mudar nome ou e-mail.

------------------- regras cadastro banda -------------------------

Na opção de montar bandas, o usuário deverá informar o número desejado de 
músicos, o instrumento de cada um dos músicos (1 por músico) e 1 gênero. 
O programa deverá exibir na tela todas as combinações possíveis de músicos
(e-mail + instrumento).

"""

# TODO: fazer funções de obteção de músicos por nome, email, genero e instrumento.

def obter_maior_id(dados: list) -> int:
    try:
        maior_id = 0
        for item in dados:
            if int(item['id']) > maior_id:
                maior_id = int(item['id'])
        return maior_id
    except KeyError:
        print('Foi encontrada uma incosistência nos dados guardados.')
    except:
        print('Erro desconhecido')

def validar_email(email:str)-> bool:
    """ Valida a sintaxe do email e busca se o email já existe no banco de dados
    irá retornar um booleano indicando se o endereço de email passado pode ser utilizado """
    if email.count('@') != 1:
        return False
    alfabeto =  list(map(chr, range(97, 123)))
    simbolos = ['@','.', '_']
    numeros = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for caracter in email:
        if caracter not in alfabeto + simbolos + numeros:
            return False
    musicos_existentes = obter_json(path_musicos)
    emails_existentes = list(map(lambda musico: musico['email'], musicos_existentes))
    if email in emails_existentes:
        return False
    return True
    
def obter_json(path: str) -> list | dict :
    """ Recebe um path de arquivo json e retorna seu conteúdo
    ou cria e retorna uma lista vazia caso o arquivo não exista.
    """
    try:
        dados = json.load(open(path))
        return dados
    except FileNotFoundError:
        print(f'Arquivo não encontrado no path: {path_bandas}')
        print('Criando arquivo...')
        return []
    
def gravar_json(data: any, path: str) -> None:
    """ Escreve as informações em um arquivo Json, recebe a informação 
    e o nome do arquivo """
    try:
        with open(path, 'w') as outfile:
            json.dump(data,
                        outfile,
                        indent=4,
                        sort_keys=True,
                        default=str,
                        ensure_ascii=False)
    except Exception as erro:
        print('Algum erro ocorreu ao salvar o arquivo')

def cadastrar_musico(musico):
    musicos_existentes = obter_json(path_musicos)
    musico['id'] = obter_maior_id(musicos_existentes) + 1
    musicos_existentes.append(musico)
    gravar_json(musicos_existentes, path_musicos)

def montar_banda(banda):
    try:
        bandas_existentes = obter_json(path_bandas)
        musicos_existentes = obter_json(path_musicos)

        for musico_id in banda['integrantes']:
            # Confere se algum dos integrantes que estão na banda
            # não existe no banco de dados
            if musico_id not in list(map(lambda musico: musico['id'], musicos_existentes)):
                raise Exception(f'Não foi encontrado músico com id {musico_id}')

        ids_banda = sorted(banda['integrantes'])

        for item in bandas_existentes:
            ids_item = sorted(item['integrantes'])
            if (ids_item == ids_banda):
                raise Exception(f'Erro: Configuração de integrantes já existe na banda "{item["nome"]}"')

            if (item['nome'] == banda['nome']):
                raise Exception(f'Erro: Nome da banda já existe na base de dados')

        bandas_existentes.append(banda)
        gravar_json(bandas_existentes, path_bandas)

    except Exception as erro:
        print(erro)

def form_musico():
    nome = input('Nome: ')
    email = input('Email: ')
    while not validar_email(email):
        print('Email inválido')
        email = input('Email: ')
    generos_musicais = []
    while True:
        if len(generos_musicais) == 0:
            print('Adicionar gênero musical: ', end='')
        else:
            print(f'Gêneros já adicionados: {", ".join(generos_musicais)}')
            print('Adicionar outro gênero musical: ', end='')
        genero = input()
        while genero == '':
            print('Valor invalido, por favor, tente novamente')
            genero = input()
        generos_musicais.append(genero.upper())
        print('Deseja adicionar outro genero musical? (s/n)')
        genero = input()
        if (genero[0]).lower() == 'n':
            break
    musico = {
        'nome': nome.upper(),
        'email': email,
        'generos_musicais': generos_musicais
    }
    return musico

def form_banda():
    banda = {
        'id': obter_maior_id(obter_json(path_bandas)) + 1,
        'nome': input('Nome: ').upper(),
        'integrantes': []
    }
    while True:
        print('Adicionar integrante: ', end='')
        integrante = input()
        while integrante == '':
            print('Valor invalido, por favor, tente novamente')
            integrante = input()
        integrante = int(integrante)
        if integrante not in map(lambda musico: musico['id'], obter_json(path_musicos)):
            print('Músico não encontrado')
            continue
        banda['integrantes'].append(integrante)
        print('Deseja adicionar outro integrante? (s/n)')
        integrante = input()
        if (integrante[0]).lower() == 'n':
            break
    return banda

def menu():
    print('1 - Cadastrar músico')
    print('2 - Cadastrar banda')
    print('3 - Sair')
    opcao = input('Opção: ')
    return opcao

def main():
    while True:
        opcao = menu()
        if opcao == '1':
            musico = form_musico()
            cadastrar_musico(musico)
        elif opcao == '2':
            banda = form_banda()
            montar_banda(banda)
        elif opcao == '3':
            break

if __name__ == '__main__':
    main()