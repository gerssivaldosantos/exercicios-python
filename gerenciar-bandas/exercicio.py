import json

path_bandas = 'bandas.json'
path_musicos = 'musicos.json'

"""

--------------------------- CheckList ----------------------------

[V] Cadastrar músicos
[V] Buscar músicos por email
[V] Buscar músicos por nome
[V] Buscar músicos por gênero musical
[V] Buscar bandas por nome - EXTRA
[V] Modificar músicos
[X] Montar bandas
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
def obter_musicos_por_ids(ids: list, musicos: list) -> list:
    resultado = []
    for id in ids:
        musico = []
        for item in filter(lambda x: x['id'] == id, musicos):
            musico.append(item)
        if len(musico)  > 0:
            resultado.append(musico[0])
    return resultado

def analisar_combinacoes(ids, n):
    if n == 0:
        return [[]]
     
    combinacoes =[]

    for i in range(0, len(ids)):

        m = ids[i]
        remIds = ids[i + 1:]
         
        restanteIds_combo = analisar_combinacoes(remIds, n-1)
        for p in restanteIds_combo:
            combinacao_id = [m, *p]
            combinacoes.append(combinacao_id)
           
    return combinacoes

def obter_musicos_por_combinacao(combinacoes):
    combinacoes_musicos = []
    for combinacao in combinacoes:
        musicos_combinacao = obter_musicos_por_ids(combinacao)
        # é trazido uma lista de objetos, a linha abaixo primeiro
        # cada objeto é um músico, cada músico tem uma lista de instrumentos
        # então é recolhido estes instrumentos, eles ficam disponizeis
        # mas será uma linha totalmente aninhada, então é usada 
        # List Comprehension para transformar em uma lista normal de strings
        # essa lista de strings contém repetições, então é feito um set para
        # remover estas repetições
        instrumentos = list(set([item for sublist in list(map(lambda musico: musico['instrumentos'], musicos_combinacao)) for item in sublist]))

        if len(instrumentos) == len(instrumentos_banda) and len(list(set(instrumentos + instrumentos_banda))) == len(instrumentos_banda):
            combinacoes_musicos.append(musicos_combinacao)
    return combinacoes_musicos



def sobrescrever_id(dado, path):
    dados_existentes = obter_json(path)
    for i in range(len(dados_existentes)):
        if dados_existentes[i]['id'] == dado['id']:
            dados_existentes[i] = dado
            break
    gravar_json(dados_existentes, path)
    
def criar_lista(listagem: str) -> list:
    """ Recebe uma string e retorna uma lista de strings separadas por vírgula."""
    return list(map(
        lambda item: item.strip().replace(' ', ''),
        " ".join(listagem.split()).upper().split(', ')))

def buscar_banda_nome(nome: str) -> list:
    bandas_existentes = obter_json(path_bandas)
    bandas_encontradas = []
    nome = nome.upper()
    for banda in bandas_existentes:
        if nome in banda['nome']:
            bandas_encontradas.append(banda)
    return bandas_encontradas

def mostrar_bandas(bandas:list) -> None:
    print(f'Número de dados encontrados: {len(bandas)}')
    for banda in bandas:
        print()
        print(f'nome: {banda["nome"]}\nmusicos: {", ".join(banda["integrantes"])} ')
    print()

def mostrar_musicos(musicos: list) -> None:
    print(f'Número de dados encontrados: {len(musicos)}')
    for musico in musicos:
        print()
        print(f'nome: {musico["nome"]}\nemail: {musico["email"]}\ngêneros: {", ".join(musico["generos_musicais"])}\nInstrumentos: {", ".join(musico["instrumentos"])}')
    print()

def buscar_musico_email(email: str) -> list:
    musicos_existentes = obter_json(path_musicos)
    for musico in musicos_existentes:
        if musico['email'] == email:
            return [musico]
    return []

def buscar_musico_nome(nome: str) -> list:
    musicos_existentes = obter_json(path_musicos)
    musicos_encontrados = []
    nome = nome.upper()
    for musico in musicos_existentes:
        if nome in musico['nome']:
            musicos_encontrados.append(musico)
    return musicos_encontrados

def buscar_musico_genero(genero: str) -> list:
    musicos_existentes = obter_json(path_musicos)
    musicos_encontrados = []
    genero = genero.upper()
    for musico in musicos_existentes:
        if genero in musico['generos_musicais']:
            musicos_encontrados.append(musico)
    return musicos_encontrados

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

def validar_banda(banda: dict) -> list:
    """ Verifica se a configuração de banda passa é passivel a ser criada, caso seja, retorna
    os musicos cadastrados que podem ser adicionados a banda. """
    try:
        bandas_existentes = obter_json(path_bandas)
        musicos_existentes = obter_json(path_musicos)
        musicos_compativeis_genero = []
        musicos_compativeis_genero_instrumento = []
        for item in bandas_existentes:
            if (item['nome'] == banda['nome']):
                raise Exception(f'Nome da banda já existe na base de dados')
        for musico in musicos_existentes:
            """ Verifica se existem músicos suficientes que tenham o gênero musical
            escolhido pela banda """
            if musico['generos_musicais']:
                if banda['genero_musical'] in list(map(lambda genero: genero, musico['generos_musicais'])):
                    musicos_compativeis_genero.append(musico)
        if len(musicos_compativeis_genero) < len(banda['instrumentos']):
            raise Exception(f'Não há musicos suficientes compatíveis com o gênero musical da banda')

        for instrumento in banda['instrumentos']:
            """ Verifica se existe músico do mesmo gênero músical da banda que toque o instrumento que ela precisa """
            listas_instrumentos_tocados = list(map(lambda musico: musico['instrumentos'], musicos_compativeis_genero))
            instrumentos_tocados = []
            for lista in listas_instrumentos_tocados:
                for item in lista:
                    instrumentos_tocados.append(item)
            if instrumento not in instrumentos_tocados:
                raise Exception(f'Não há musicos que possam tocar o instrumento {instrumento}')
        for musico in musicos_compativeis_genero:
            for instrumento in musico['instrumentos']:
                if instrumento in banda['instrumentos']:
                    musicos_compativeis_genero_instrumento.append(musico)
                    break
        return musicos_compativeis_genero_instrumento
    except Exception as erro:
        print(f"Erro: {erro}")
        return []

def form_montar_banda(musicos: list, banda: list) -> dict:
    """ retorna todas as possibilidades de combinações possiveis de banda considerando os instrumentos """
    if len(musicos) > 0:
        
        for instrumento in banda['instrumentos']:
            musicos_instrumento = list(filter(lambda musico: instrumento in musico['instrumentos'], musicos))
            print("Seleção de músicos para integrar a banda")
            if len(musicos_instrumento) > 0:
                # Caso existam músicos que tocam o instrumento, exibe a lista de músicos
                print(f'Músicos que tocam {instrumento.lower()}')
                for i in range(len(musicos_instrumento)):
                    print(f'[ {i} ]{musicos_instrumento[i]["nome"]}({musicos_instrumento[i]["email"]})')
                # Pergunta ao usuário qual músico ele deseja adicionar à banda
                parar = False
                while not parar:
                    try:
                        resposta = int(input(f'Digite o número do músico que deseja adicionar à banda: '))
                        if resposta < 0 or resposta >= len(musicos_instrumento):
                            raise Exception('Número inválido')
                        parar = True
                    except Exception as erro:
                        print(f'Erro: {erro}')
                # Adiciona o músico à banda
                banda['integrantes'].append(musicos_instrumento[resposta]['id'])
                musicos = list(filter(lambda musico: musico['id'] != musicos_instrumento[resposta]['id'], musicos))
        if (len(banda['instrumentos']) != len(banda['integrantes'])):
            raise Exception('Não foi possível montar a banda. Pela ordem das escolhas de integrantes ')
            print('( Algum instrumento ficou sem músico, isso pode ser contornando escolhendo outra configuração de banda )')
        print(f'Banda {banda["nome"]} criada com sucesso!')
        bandas = obter_json(path_bandas)
        bandas.append(banda)
        gravar_json(bandas, path_bandas)


def criar_combinacoes_bandas():
    # TODO: criar lógica para criar configurações possiveis de integrantes na banda
    pass 

def form_musico():
    nome = input('Nome: ')
    email = input('Email: ')
    while not validar_email(email):
        print('Email inválido')
        email = input('Email: ')
    generos_musicais = criar_lista(input('Gêneros musicais (separados por vírgula): '))
    instrumentos = criar_lista(input('Instrumentos (separados por vírgula): '))
    musico = {
        'nome': nome.upper(),
        'email': email,
        'generos_musicais': generos_musicais,
        'instrumentos': instrumentos
    }
    return musico

def form_banda():
    parar = False
    instrumentos = []
    nome = input('Nome: ').upper()
    genero = ''
    while parar != True:
        numero_integrantes = int(input('Número de integrantes da banda: '))
        if numero_integrantes == 0:
            print('Número invalido')
        else:
            while numero_integrantes != len(instrumentos):
                instrumentos = criar_lista(input('Instrumentos (separados por vírgula): '))
                instrumentos = sorted(set(instrumentos))
                if len(instrumentos) != numero_integrantes:
                    print('Valores inválidos, é permitido somente 1 instrumento por integrante, e somente 1 instrumento de cada tipo')
        while genero == '':
            genero = input('Gênero musical: ')
        parar = True
    banda = {
        'id': obter_maior_id(obter_json(path_bandas)) + 1,
        'nome': nome.upper(),
        'integrantes': [],
        'genero_musical': genero.upper(),
        'instrumentos': instrumentos
    }
    return banda

def menu():
    print(f'\n------- MENU -------')
    print('1 - Cadastrar músico')
    print('2 - Editar Dados do músico')
    print('3 - Buscar Músicos')
    print('4 - Buscar Bandas')
    print('5 - Cadastrar banda')
    print('0 - Sair')
    opcao = input('Opção: ')
    if opcao == '3':
        print('1 - Buscar por nome')
        print('2 - Buscar por gênero musical')
        print('3 - Buscar por email')
        opcao += '.' + input('Opção: ')
    return opcao

def main():
    sair = False
    while not sair:
        opcao = menu()
        if opcao == '1':
            musico = form_musico()
            cadastrar_musico(musico)
        elif opcao == '2':
            musico = buscar_musico_email(input('Email: '))
            if musico is []:
                print('Músico não encontrado')
                continue
            mostrar_musicos(musico)
            musico = musico[0]
            print('1 - Adicionar gêneros musicais')
            print('2 - Adicionar instrumentos')
            print('3 - Remover gêneros musicais')
            print('4 - Remover instrumentos')
            print('5 - Cancelar')
            opcao = input('Opção: ')
            if opcao == '1':
                generos = input('Gêneros musicais (separados por vírgula): ')
                generos = criar_lista(generos)
                musico['generos_musicais'] += generos
                sobrescrever_id(musico, path_musicos)
            elif opcao == '2':
                instrumentos = input('Instrumentos (separados por vírgula): ')
                instrumentos = criar_lista(instrumentos)
                musico['instrumentos'] += instrumentos
                sobrescrever_id(musico, path_musicos)
            elif opcao == '3':
                while (opcao != 'n'):
                    for i in range(len(musico['generos_musicais'])):
                        print(f'{i} - {musico["generos_musicais"][i]}')
                    index_genero = int(input('Digite o índice do gênero musical que deseja remover: '))
                    musico['generos_musicais'].pop(index_genero)
                    sobrescrever_id(musico, path_musicos)
                    opcao = input('Deseja remover outro gênero musical? (s/n) ')
            elif opcao == '4':
                while (opcao != 'n'):
                    for i in range(len(musico['instrumentos'])):
                        print(f'{i} - {musico["instrumentos"][i]}')
                    index_instrumento = int(input('Digite o índice do instrumento que deseja remover: '))
                    musico['instrumentos'].pop(index_instrumento)
                    sobrescrever_id(musico, path_musicos)
                    opcao = input('Deseja remover outro instrumento? (s/n) ')
            
        elif opcao == '3.1':
            mostrar_musicos(buscar_musico_nome(input('Digite o nome do músico: ')))
        elif opcao == '3.2':
            mostrar_musicos(buscar_musico_genero(input('Digite o gênero músical: ')))
        elif opcao == '3.3':
            mostrar_musicos(buscar_musico_email(input('Digite o email do músico: ')))
        elif opcao == '4':
            mostrar_bandas(buscar_banda_nome(input('Digite o nome da banda: ')))
        elif opcao == '5':
            banda = form_banda()
            musicos = validar_banda(banda)
            banda = form_montar_banda(musicos, banda)
        elif opcao == '0':
            sair = True

if __name__ == '__main__':
    main()