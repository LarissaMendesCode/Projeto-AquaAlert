

from functools import reduce

def calcular_consumo_chuveiro(tempobanho, qtdebanho):
    return qtdebanho * tempobanho * 0.2 * 60

def calcular_consumo_torneira(tempo_torneira_maos, qtdeusotorneiramaos, 
                              tempo_torneira_escovardentes, qtdeusotorneiradentes, 
                              tempo_torneira_lavarlouça, qtdeusotorneiralouça, arejador):
    
    fator = 0.15 if arejador == 1 else 0.30
    
    consumos = map(lambda t_q: t_q[0] * t_q[1] * fator * 60, [
        (tempo_torneira_maos, qtdeusotorneiramaos),
        (tempo_torneira_escovardentes, qtdeusotorneiradentes),
        (tempo_torneira_lavarlouça, qtdeusotorneiralouça),
    ])
    
    return sum(consumos)

def calcular_consumo_descarga(qtdedescarga):
    return 6 * qtdedescarga

def calcular_desperdicio(consumo, limite):
    return max(consumo - limite, 0)

def calcular_economia(consumo, limite):
    return max(limite - consumo, 0)

def calcular_fatura(volume, esgoto, categoria):
    faixas = {
        1: [2.12, None, None, None, None, None],
        2: [4.34, 7.38, 8.00, 13.77, 24.54],
        3: [6.17, 8.00, 8.65, 14.85, 26.22]
    }
    
    def calcular_valor(volume, valores):
        faixas_limites = [10, 5, 5, 5, float('inf')]
        return reduce(lambda acc, v: acc + min(volume, v[0]) * v[1], zip(faixas_limites, valores), 0)
    
    consumo_RS = calcular_valor(volume, faixas[categoria])
    esgoto_RS = calcular_valor(esgoto, faixas[categoria])
    
    return consumo_RS, esgoto_RS, consumo_RS + esgoto_RS

def coletar_dados():
    nome = input("Informe o seu nome: ")

    tempobanho = float(input("Tempo médio de banho (min): "))
    qtdebanho = int(input("Número de banhos/dia: "))

    tempo_torneira_maos = float(input("Tempo para lavar as mãos (min): "))
    qtdeusotorneiramaos = int(input("Frequência de lavar as mãos/dia: "))

    tempo_torneira_escovardentes = float(input("Tempo para escovar os dentes (min): "))
    qtdeusotorneiradentes = int(input("Frequência de escovar os dentes/dia: "))

    tempo_torneira_lavarlouça = float(input("Tempo para lavar louça (min): "))
    qtdeusotorneiralouça = int(input("Frequência de lavar louça: "))

    arejador = int(input("1. Torneira com arejador\n2. Torneira sem arejador\n"))

    qtdedescarga = int(input("Número de descargas/dia: "))

    return {
        "tempobanho": tempobanho, "qtdebanho": qtdebanho,
        "tempo_torneira_maos": tempo_torneira_maos, "qtdeusotorneiramaos": qtdeusotorneiramaos,
        "tempo_torneira_escovardentes": tempo_torneira_escovardentes, "qtdeusotorneiradentes": qtdeusotorneiradentes,
        "tempo_torneira_lavarlouça": tempo_torneira_lavarlouça, "qtdeusotorneiralouça": qtdeusotorneiralouça,
        "arejador": arejador, "qtdedescarga": qtdedescarga
    }

def main():
    dados = coletar_dados()
    
    consumo_chuveiro = calcular_consumo_chuveiro(dados["tempobanho"], dados["qtdebanho"])
    consumo_torneira = calcular_consumo_torneira(dados["tempo_torneira_maos"], dados["qtdeusotorneiramaos"], 
                                                 dados["tempo_torneira_escovardentes"], dados["qtdeusotorneiradentes"], 
                                                 dados["tempo_torneira_lavarlouça"], dados["qtdeusotorneiralouça"], 
                                                 dados["arejador"])
    consumo_descarga = calcular_consumo_descarga(dados["qtdedescarga"])

    desperdicio_chuveiro = calcular_desperdicio(consumo_chuveiro, 48)
    desperdicio_torneira = calcular_desperdicio(consumo_torneira, 27)
    desperdicio_descarga = calcular_desperdicio(consumo_descarga, 30)

    desperdicio_total = sum([desperdicio_chuveiro, desperdicio_torneira, desperdicio_descarga])
    desperdicio_total_m3 = (desperdicio_total / 1000) * 30

    opcao = int(input("1. Sair\n2. Ver Resultado\n"))
    
    if opcao == 1:
        print("Até logo!")
        return
    
    volumeatual = float(input("Volume m³ da fatura atual: "))
    reais_atual = float(input("Valor da conta atual (R$): "))

    volume = max(volumeatual - desperdicio_total_m3, 0)
    esgoto = round(volume * 0.8)

    categoria = int(input("1. Residencial Social\n2. Residencial Popular\n3. Residencial Normal\nInforme a categoria: "))
    
    if categoria not in [1, 2, 3]:
        print("Opção inválida.")
        return
    
    consumo_RS, esgoto_RS, total_RS = calcular_fatura(volume, esgoto, categoria)

    print(f"Total da fatura água (R$): {round(consumo_RS, 2)}")
    print(f"Total da fatura de esgoto (R$): {round(esgoto_RS, 2)}")
    print(f"Total da fatura (água e esgoto) (R$): {round(total_RS, 2)}")

    valoreconomia = reais_atual - total_RS
    print(f"Total economia (R$): {round(valoreconomia, 2)}")

if __name__ == "__main__":
    main()
