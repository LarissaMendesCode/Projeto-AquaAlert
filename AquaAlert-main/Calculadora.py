import sys 
from functools import reduce
import sqlite3

# Isso garante que caracteres especiais sejam interpretados corretamente ao ler e imprimir dados.
def configure_io():
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')

# Função lambda que calcula o volume de esgoto com base no volume de água consumida.
calcular_esgoto = lambda volume: round(volume * 0.8)

# Solicita que o usuário escolha uma das categorias e retorna a opção escolhida como um número inteiro.
def obter_categoria():
    print("1. Residencial Social")
    print("2. Residencial Popular")
    print("3. Residencial Normal")
    return int(input("Informe a categoria: "))

# Calcula o valor da fatura baseado no volume de consumo e nas faixas tarifárias.
def calcular_fatura(volume, faixas):
    # O volume é distribuído entre diferentes faixas de consumo.
    limites = [10, 5, 5, 30] + [None]
    valores = zip(faixas, limites)
    # Usa atribuição em expressão (:=) para atualizar volume enquanto itera. Se não houver um limite (None), todo o volume restante é cobrado na última faixa.
    valor_parcial = [(min(volume, limite) if limite else volume) * preco for preco, limite in valores if (volume := volume - (min(volume, limite) if limite else volume)) >= 0]
    return sum(valor_parcial)

# Define as faixas tarifárias de consumo de água para cada categoria.
def calcular_consumo(categoria, volume):
    faixas = {
        1: [2.12],
        2: [4.34, 7.38, 8.00, 13.77, 24.54],
        3: [6.17, 8.00, 8.65, 14.85, 26.22]
    }
    return calcular_fatura(volume, faixas.get(categoria, []))

# Utiliza a mesma lógica de calcular_consumo(), mas aplicada ao volume de esgoto.
def calcular_esgoto_fatura(categoria, esgoto):
    faixas_esgoto = {
        1: [2.12],
        2: [4.34, 7.38, 8.00, 13.77, 24.54],
        3: [6.17, 8.00, 8.65, 14.85, 26.22]
    }
    return calcular_fatura(esgoto, faixas_esgoto.get(categoria, []))
    # return calcular_consumo(categoria, esgoto)

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
    
    print(f"Total do desperdicio: {round(desperdicio_total_m3, 2)} m³")
    novo_volume = volume - desperdicio_total_m3
    print(f"Novo m³ do volume: {round(novo_volume, 2)} m³")
    novo_esgoto = calcular_esgoto(novo_volume)
    categoria = obter_categoria()
    
    novo_consumo_RS = calcular_consumo(categoria, novo_volume)
    novo_esgoto_RS = calcular_esgoto_fatura(categoria, novo_esgoto)
    novo_total_RS = novo_consumo_RS + novo_esgoto_RS
    
    print(f"Total da fatura água (R$): {round(novo_consumo_RS, 2)}")
    print(f"Total da fatura de esgoto (R$): {round(novo_esgoto_RS, 2)}")
    print(f"Total da fatura (água e esgoto) (R$): {round(novo_total_RS, 2)}")

    Economia = total_RS - novo_total_RS

    print(f"Economia (R$): {round(Economia, 2)}")
    
    # Conectar ao banco de dados (ou criar um se não existir)
conn = sqlite3.connect("consumo_agua.db")
cursor = conn.cursor()

# Criar a tabela para armazenar os dados da fatura
cursor.execute("""
CREATE TABLE IF NOT EXISTS fatura (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    volume REAL,
    esgoto REAL,
    categoria INTEGER,
    total_fatura REAL,
    economia REAL
)
""")
conn.commit()

def salvar_fatura(nome, volume, esgoto, categoria, total_fatura, economia):
    """Salva os dados da fatura no banco de dados"""
    cursor.execute("""
    INSERT INTO fatura (nome, volume, esgoto, categoria, total_fatura, economia)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, volume, esgoto, categoria, total_fatura, economia))
    conn.commit()

def listar_faturas():
    """Lista todas as faturas salvas no banco"""
    cursor.execute("SELECT * FROM fatura")
    for row in cursor.fetchall():
        print(row)

# Exemplo de como usar as funções
nome = "julia"
volume = 20.5
esgoto = 16.4
categoria = 2
total_fatura = 150.75
economia = 20.0

salvar_fatura(nome, volume, esgoto, categoria, total_fatura, economia)
listar_faturas()

# Fechar a conexão quando terminar
conn.close()



if __name__ == "__main__":
    main()
