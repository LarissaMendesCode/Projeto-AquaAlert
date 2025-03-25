
import sys

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

# Coleta entrada do usuário, realiza os cálculos e exibe os valores da fatura.
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

# Garante que main() seja executada apenas quando o script for rodado diretamente.
if __name__ == "_main_":
    main()