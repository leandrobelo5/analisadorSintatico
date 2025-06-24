import re

# Definições dos tokens e seus códigos
OPERADORES = {
    '+': 'Sim_adição',
    '-': 'Sim_subtração',
    '*': 'Sim_multiplicação',
    '/': 'Sim_divisão'
}

def tokenize(expr):
    tokens = []
    expr = expr.replace(' ', '')  # remover espaços

    pattern = r'\d+\.\d+|\d+|[\+\-\*/\(\)]'
    partes = re.findall(pattern, expr)

    for parte in partes:
        if parte.isdigit():
            tokens.append((parte, 'Identificador'))
        elif re.fullmatch(r'\d+\.\d+', parte):
            tokens.append((parte, 'Identificador'))
        elif parte in OPERADORES:
            tokens.append((parte, OPERADORES[parte]))
        elif parte == '(':
            tokens.append((parte, 'Abre_parênteses'))
        elif parte == ')':
            tokens.append((parte, 'Fecha_parênteses'))
        else:
            tokens.append((parte, 'Desconhecido'))

    return tokens

def print_token_table(tokens):
    print('\nTabela de Tokens:')
    print(f'{"Token":<10} | Código')
    print('-' * 25)
    for tok, tipo in tokens:
        print(f'{tok:<10} | {tipo}')

def gerar_derivacao(expr):
    print("\nDerivação segundo G1:")
    def derivar(expr):
        def is_number(token):
            return re.fullmatch(r'\d+(\.\d+)?', token) is not None

        stack = expr.replace(' ', '')
        result = []
        i = 0
        n = len(stack)

        def parse_E():
            nonlocal i
            r = []

            r.append("E → I")
            r += parse_I()

            if i < n and stack[i] in OPERADORES:
                op = stack[i]
                r[0] = "E → I O E"
                r.append(f"O → {op}")
                i += 1
                r += parse_E()
            return r

        def parse_I():
            nonlocal i
            if i < n:
                if stack[i] == '(':
                    r = ["I → N", "N → (E)"]
                    i += 1
                    r += parse_E()
                    if i < n and stack[i] == ')':
                        r.append(")")
                        i += 1
                    else:
                        r.append("Erro: parêntese não fechado")
                    return r
                elif stack[i].isdigit():
                    number = ''
                    while i < n and (stack[i].isdigit() or stack[i] == '.'):
                        number += stack[i]
                        i += 1
                    r = ["I → N", f"N → {number}"]
                    return r
            return ["Erro na análise"]

        return parse_E()

    for step in derivar(expr):
        print(step)

# Execução principal com loop interativo
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

        tokens = tokenize(expressao)
        print_token_table(tokens)
        gerar_derivacao(expressao)
        print("\n" + "=" * 40 + "\n")
