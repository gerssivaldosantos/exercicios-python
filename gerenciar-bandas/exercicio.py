""" Para implementar o programa abaixo, tente empregar técnicas estudadas no módulo atual quando possível: tratamento de 
strings, manipulação de arquivos utilizando as bibliotecas auxiliares estudadas (csv e json), tratamento de exceção, diferentes 
formatos de parâmetro de função, compreensão de listas e/ou geradores, funções de alta ordem e lambda. Apesar de ser possível 
resolver boa parte dos problemas utilizando loops e técnicas do módulo anterior, você deixará de treinar os novos conceitos e
 perderá a oportunidade de receber feedback adequado sobre o seu aprendizado deste módulo.

Uma grande dificuldade de muitos músicos de garagem é encontrar outros músicos que toquem instrumentos diferentes, possuam gostos 
semelhantes e disponibilidade para formar conjuntos.

Vamos fazer um sistema para auxiliar na formação de bandas online! Em seu menu principal, o programa deverá oferecer as seguintes 
funcionalidades:

Cadastrar músicos
Buscar músicos
Modificar músicos
Montar bandas
Sair
No cadastro devem ser digitadas as seguintes informações:

Nome (string contendo apenas letras e espaço)
E-mail (string contendo apenas letras, underscore (_), ponto (.), dígitos numéricos e, obrigatoriamente, exatamente 1 arroba (@))
Gêneros musicais (mínimo 1, usuário pode digitar quantos forem necessários)
Instrumentos (mínimo 1, usuário pode digitar quantos forem necessários)
As entradas devem ser validadas seguindo as regras. O e-mail deve ser único: se ele já existe, o cadastro não deve ser concluído.

DICA: padronize suas strings na hora de salvar em sua base para evitar que buscas sejam prejudicadas por divergências de maiúsculas
 e minúsculas.

Na busca o usuário deve passar pelo menos 1 das opções: nome, e-mail, gênero (digitar apenas 1) ou instrumento (digitar apenas 1). 
O usuário deve selecionar se os resultados devem bater com todas as informações digitadas ou pelo menos uma (ex: se o usuário digitar nome 
e instrumento, a busca pode ser por resultados contendo o nome E o instrumento vs o nome OU o instrumento).

Na modificação de um usuário, será feita uma busca especificamente por e-mail. É permitido adicionar ou remover gêneros e instrumentos. 
Não é permitido mudar nome ou e-mail.

Na opção de montar bandas, o usuário deverá informar o número desejado de músicos, o instrumento de cada um dos músicos (1 por músico) e 1 gênero. 
O programa deverá exibir na tela todas as combinações possíveis de músicos (e-mail + instrumento). """

import json

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
    
    return False

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