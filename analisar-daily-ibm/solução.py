import csv

def obterMaiorOsc(nomeArquivo):
    with open(nomeArquivo) as arquivo:
        dados = list(csv.reader(arquivo, delimiter=','))[1:]
        maior = 0
        for dado in dados:
            oscilacao = float(dado[2]) - float(dado[3])    
            if oscilacao > maior:
                maior = oscilacao
                dia = dado
        print(f"""A maior oscilação aconteceu no dia {dia[0]}
    O maior valor foi {dia[2]}
    O menor valor foi {dia[3]}""")

obterMaiorOsc('daily_IBM.csv')