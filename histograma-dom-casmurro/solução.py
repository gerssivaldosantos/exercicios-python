def limpa_linha(linha: str) -> list:
    """
    Recebe uma linha de texto e retorna uma lista de palavras.
    """
    processado = linha.lower().split()
    for i in range(len(processado) - 1):
          processado[i] = processado[i].strip('.,;:?!_»-')

    return processado

with open('domcasmurro.txt', encoding='utf-8') as arquivo:
    texto = arquivo.read()
    palavras_texto = limpa_linha(texto)
    histograma = dict()

    for palavra in palavras_texto:
        if palavra in histograma.keys():
            histograma[palavra] += 1
        else:
            histograma[palavra] = 1
    
    print(histograma)