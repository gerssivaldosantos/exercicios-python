import json
import re 

bandas = [
    {
        'id': 1,
        'nome': 'Metallica',
        'integrantes': [
            1,
            3,
            4,
            5,
            6
        ]
    }
]

path_bandas = 'bandas.json'
path_musicos = 'musicos.json'

# TODO: criar função "maior id" que recebe um json e e retorna o maior id da banda ou musico
# isso vai ser usado na geração de novos ids quando cadastrar banda ou id

# TODO: refatorar a inserção de nova banda em uma função separada do menu

# TODO: fazer funções de obteção de bandas e musicos existentes e funções para exclui-los

def validar_email(email:str)-> bool:
    """ Valida a sintaxe do email e busca se o email já existe no banco de dados
    irá retornar um booleano indicando se o endereço de email passado pode ser utilizado """
    musicos_existentes = obter_json(path_musicos)
    emails_existentes = list(map(lambda musico: musico['email'], musicos_existentes))
    if email in emails_existentes:
        return False
    return bool(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email))

def obter_json(path: str) -> list | dict :
    """ Recebe um path de arquivo json e retorna seu conteúdo
    ou cria e retorna uma lista vazia caso o arquivo não exista.
    """
    try:
        dados = json.load(open(path))
        return dados
    except FileNotFoundError:
        return []
        print(f'Arquivo não encontrado no path: {path_bandas}')
        print('Criando arquivo...')
    
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
    musicos_existentes.append(musico)
    musico['id'] = len(musicos_existentes)
    gravar_json(musicos_existentes, path_musicos)

def montar_banda(banda):
    try:
        bandas_existentes = obter_json(path_bandas)
        musicos_existentes = obter_json(path_musicos)

        for musico_id in banda['integrantes']:
            # Confere se algum dos integrantes que estão na banda
            # não existe no banco de dados
            if musico_id not in map(lambda musico: musico['id'], musicos_existentes):
                raise Exception(f'Não foi encontrado músico com id {musico_id}')

        for item in bandas_existentes:
            ids_item = sorted(item['integrantes'])
            ids_banda = sorted(banda['integrantes'])

            if (ids_item == ids_banda):
                raise Exception(f'Erro: Configuração de integrantes já existe na banda "{item["nome"]}"')

            if (item['nome'] == banda['nome']):
                raise Exception(f'Erro: Nome da banda já existe na base de dados')

        banda['id'] = len(bandas_existentes) + 1
        bandas.append(banda)
        gravar_json(bandas, path_bandas)

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
            banda = {
                'id': len(obter_json(path_bandas)) + 1,
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
                    print('Integrante não encontrado')
                    continue
                banda['integrantes'].append(integrante)
                print('Deseja adicionar outro integrante? (s/n)')
                integrante = input()
                if (integrante[0]).lower() == 'n':
                    break
            montar_banda(banda)
        elif opcao == '3':
            break

if __name__ == '__main__':
    main()