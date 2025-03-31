import sys 
from functools import reduce

def configure_io():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

calcular_esgoto = lambda volume: round(volume * 0.8)

def obter_categoria():
    print("1. Residencial Social")
    print("2. Residencial Popular")
    print("3. Residencial Normal")
    return int(input("Informe a categoria: "))

def calcular_fatura(volume, faixas):
    limites = [10, 5, 5, 30] + [None]
    valores = zip(faixas, limites)
    valor_parcial = [(min(volume, limite) if limite else volume) * preco for preco, limite in valores if (volume := volume - (min(volume, limite) if limite else volume)) >= 0]
    return sum(valor_parcial)

def calcular_consumo(categoria, volume):
    faixas = {
        1: [2.12],
        2: [4.34, 7.38, 8.00, 13.77, 24.54],
        3: [6.17, 8.00, 8.65, 14.85, 26.22]
    }
    return calcular_fatura(volume, faixas.get(categoria, []))

def calcular_esgoto_fatura(categoria, esgoto):
    faixas_esgoto = {
        1: [2.12],
        2: [4.34, 7.38, 8.00, 13.77, 24.54],
        3: [6.17, 8.00, 8.65, 14.85, 26.22]
    }
    return calcular_fatura(esgoto, faixas_esgoto.get(categoria, []))

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

def criar_calculadora_desperdicio(limite):
    return lambda consumo: max(consumo - limite, 0)

calcular_desperdicio_chuveiro = criar_calculadora_desperdicio(48)
calcular_desperdicio_torneira = criar_calculadora_desperdicio(27)
calcular_desperdicio_descarga = criar_calculadora_desperdicio(30)

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
    qtdedescarga = int(input("Número de descargas/dia: "))
    print("Os valores utilizados para o cálculo são apenas uma referência. O consumo pode variar de acordo com a pressão da água e o tipo de abertura da torneira ou do equipamento")
    return {
        "tempobanho": tempobanho, "qtdebanho": qtdebanho,
        "tempo_torneira_maos": tempo_torneira_maos, "qtdeusotorneiramaos": qtdeusotorneiramaos,
        "tempo_torneira_escovardentes": tempo_torneira_escovardentes, "qtdeusotorneiradentes": qtdeusotorneiradentes,
        "tempo_torneira_lavarlouça": tempo_torneira_lavarlouça, "qtdeusotorneiralouça": qtdeusotorneiralouça, "qtdedescarga": qtdedescarga
    }

def main():
    configure_io()
    volume = float(input("Informe o volume m³ da sua fatura: "))
    esgoto = calcular_esgoto(volume)
    categoria = obter_categoria()
    
    consumo_RS = calcular_consumo(categoria, volume)
    esgoto_RS = calcular_esgoto_fatura(categoria, esgoto)
    total_RS = consumo_RS + esgoto_RS
    
    print(f"Total da fatura água (R$): {round(consumo_RS, 2)}")
    print(f"Total da fatura de esgoto (R$): {round(esgoto_RS, 2)}")
    print(f"Total da fatura (água e esgoto) (R$): {round(total_RS, 2)}")
    
    dados = coletar_dados()
    consumo_chuveiro = calcular_consumo_chuveiro(dados["tempobanho"], dados["qtdebanho"])
    desperdicio_chuveiro = calcular_desperdicio_chuveiro(consumo_chuveiro)
    desperdicio_total = desperdicio_chuveiro
    desperdicio_total_m3 = (desperdicio_total / 1000) * 30
    
    print(f"Total do desperdício: {round(desperdicio_total_m3, 2)} m³")
    novo_volume = volume - desperdicio_total_m3
    print(f"Novo m³ do volume: {round(novo_volume, 2)} m³")
    
    novo_esgoto = calcular_esgoto(novo_volume)
    novo_consumo_RS = calcular_consumo(categoria, novo_volume)
    novo_esgoto_RS = calcular_esgoto_fatura(categoria, novo_esgoto)
    novo_total_RS = novo_consumo_RS + novo_esgoto_RS
    
    print(f"Total da fatura água (R$): {round(novo_consumo_RS, 2)}")
    print(f"Total da fatura de esgoto (R$): {round(novo_esgoto_RS, 2)}")
    print(f"Total da fatura (água e esgoto) (R$): {round(novo_total_RS, 2)}")
    
    economia = total_RS - novo_total_RS
    print(f"Economia (R$): {round(economia, 2)}")
    print("A ONU recomenda 110 litros/0,11 m³ por dia para consumo básico e higiene pessoal.")

if __name__ == "__main__":
    main()
