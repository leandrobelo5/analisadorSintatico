import re  # Módulo de expressões regulares, usado para identificar padrões nos tokens

# Dicionário com os símbolos e os respectivos nomes dos operadores
OPERADORES = {
    '+': 'Sim_adição',
    '-': 'Sim_subtração',
    '*': 'Sim_multiplicação',
    '/': 'Sim_divisão'
}

# Função que recebe uma expressão e gera a lista de tokens
def tokenize(expr):
    tokens = []
    expr = expr.replace(' ', '')  # Remove espaços em branco da expressão

    # Expressão regular para encontrar números inteiros, decimais, operadores e parênteses
    pattern = r'\d+\.\d+|\d+|[\+\-\*/\(\)]'
    partes = re.findall(pattern, expr)  # Divide a expressão em partes com base no padrão

    for parte in partes:
        if parte.isdigit():  # Se é um número inteiro
            tokens.append((parte, 'Identificador'))
        elif re.fullmatch(r'\d+\.\d+', parte):  # Se é número decimal
            tokens.append((parte, 'Identificador'))
        elif parte in OPERADORES:  # Se é um operador
            tokens.append((parte, OPERADORES[parte]))
        elif parte == '(':  # Abre parêntese
            tokens.append((parte, 'Abre_parênteses'))
        elif parte == ')':  # Fecha parêntese
            tokens.append((parte, 'Fecha_parênteses'))
        else:  # Qualquer outro símbolo não reconhecido
            tokens.append((parte, 'Desconhecido'))

    return tokens  # Retorna a lista de tokens

# Função que imprime a tabela de tokens formatada
def print_token_table(tokens):
    print('\nTabela de Tokens:')
    print(f'{"Token":<10} | Código')
    print('-' * 25)
    for tok, tipo in tokens:
        print(f'{tok:<10} | {tipo}')

# Função principal de derivação sintática com base na gramática G1
def gerar_derivacao(expr):
    print("\nDerivação segundo G1:")

    # Função interna que realiza a análise sintática
    def derivar(expr):
        stack = expr.replace(' ', '')  # Remove espaços
        i = 0  # Posição atual do "cursor" na expressão
        n = len(stack)

        # Função para analisar expressões (E)
        def parse_E():
            nonlocal i
            r = []

            r.append("E → I")  # Assume que é só um identificador por padrão
            r += parse_I()  # Analisa I

            # Verifica se ainda há um operador e uma próxima expressão
            if i < n and stack[i] in OPERADORES:
                op = stack[i]
                r[0] = "E → I O E"  # Ajusta a derivação
                r.append(f"O → {op}")  # Mostra o operador
                i += 1
                r += parse_E()  # Continua analisando a próxima parte da expressão
            return r

        # Função para analisar I (Identificador ou Número)
        def parse_I():
            nonlocal i
            if i < n:
                if stack[i] == '(':  # Caso tenha um parêntese
                    r = ["I → N", "N → (E)"]
                    i += 1
                    r += parse_E()  # Analisa o que está dentro do parêntese
                    if i < n and stack[i] == ')':
                        r.append(")")  # Fecha parêntese reconhecido
                        i += 1
                    else:
                        r.append("Erro: parêntese não fechado")
                    return r
                elif stack[i].isdigit():  # Se for um número
                    number = ''
                    while i < n and (stack[i].isdigit() or stack[i] == '.'):
                        number += stack[i]
                        i += 1
                    r = ["I → N", f"N → {number}"]
                    return r
            return ["Erro na análise"]  # Se não reconhece, retorna erro

        return parse_E()  # Inicia a análise da expressão pelo símbolo inicial E

    # Imprime os passos da derivação linha por linha
    for step in derivar(expr):
        print(step)

# Função principal que mantém o programa em loop até o usuário digitar "sair"
if __name__ == '__main__':
    print("Digite expressões matemáticas (digite 'sair' para encerrar):\n")
    while True:
        expressao = input("Expressão: ").strip()
        if expressao.lower() == 'sair':
            print("Encerrando o programa.")
            break
        if not expressao:
            print("Expressão vazia. Tente novamente.")
            continue

        tokens = tokenize(expressao)  # Analisa léxicamente
        print_token_table(tokens)     # Mostra os tokens
        gerar_derivacao(expressao)    # Aplica a gramática
        print("\n" + "=" * 40 + "\n")  # Separador visual
