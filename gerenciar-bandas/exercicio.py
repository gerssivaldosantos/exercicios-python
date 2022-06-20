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

def validar_email(email:str)-> bool:
    return bool(re.search('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$',email))

def obter_json(path: str) -> list | dict :
    """ recive the path of anywhere json and return
    an list of content
    str -> anything
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
    e o nome do arquivo que será salvo em "outputs" """

    with open(path, 'w') as outfile:
        json.dump(data,
                    outfile,
                    indent=4,
                    sort_keys=True,
                    default=str,
                    ensure_ascii=False)

def cadastrar_musico(musico):
    musicos_existentes = obter_json(path_musicos)
    musicos_existentes.append(musico)
    musico['id'] = len(musicos_existentes)
    gravar_json(musicos_existentes, path_musicos)

def montar_banda(banda):
    try:
        bandas_existentes = obter_json(path_bandas)
        musicos_existentes = obter_json(path_musicos)
        
        if bandas_existentes and musicos_existentes:

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
    #TODO: verificar a existência do email no banco de dados
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
        generos_musicais.append(genero)
        print('Deseja adicionar outro genero musical? (s/n)')
        genero = input()
        if (genero[0]).lower() == 'n':
            break
    musico = {
        'nome': nome,
        'email': email,
        'generos_musicais': generos_musicais
    }
    return musico
        
form_musico()