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

def obter_json(path: str) -> list | dict | None:
    """ recive the path of anywhere json and return
    an list of content
    str -> anything
    """
    try:
        dados = json.load(open(path))
        return dados
    except FileNotFoundError:
        print(f'Arquivo não encontrado no path: {path_bandas}')
    
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


montar_banda({'id': 1, 'nome': 'Tunico e tinoco', 'integrantes': [3]})