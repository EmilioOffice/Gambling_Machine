import random as random

MAX_NUMBRE_OF_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLUMNS = 3

symbol_count = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}

symbol_value = {
    'A': 5,
    'B': 4,
    'C': 3,
    'D': 2
}

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
            
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1) 
            
    return winnings, winning_lines


def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbols, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbols)
    
    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        
        columns.append(column)

    return columns

def print_slot_machine(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(column[row], end=" | ")
            else:
                print(column[row], end="")
                
        print()

def deposit():
    while True:
        amount = input("Ingrese el monto que le gustaria depositar: $")
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                break
            else:
                print("El monto debe ser mayor a 0.")
        else:
            print("El monto ingresado no es numerico, por favor intentalo denuevo.")
    
    return amount


def get_number_of_lines():
    while True:
        lines = input("Ingrese el numero de lineas a las que les desea apostar: (1-" + str(MAX_NUMBRE_OF_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_NUMBRE_OF_LINES:
                break
            else:
                print("El numero de lineas no es valido.")
        else:
            print("El monto ingresado no es numerico, por favor intentalo denuevo.")
    
    return lines

def get_bet():
    while True:
        amount = input("Ingrese el monto que le gustaria apostar en cada linea: $")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            else:
                print(f"El monto debe ser mayor a ${MIN_BET} y menor a ${MAX_BET}.")
        else:
            print("El monto ingresado no es numerico, por favor intentalo denuevo.")
    
    return amount

def spin(balance):
    lines = get_number_of_lines()
    while True:
        bet = get_bet()
        total_bet = bet * lines
        if total_bet > balance:
            if balance <= 0:
                print("Ya no cuenta con un balance.")
                resp = input("Le gustaria depositar en su cuenta: (S = si | N = no)")
                if resp.lower() != "n":
                    return "¡Muchas gracias por jugar, que tenga un buen dia!"
            else:
                print(f"El monto total de la apuesta es mayor a su balance.\nSu balance actual es de ${balance}.")
        else:
            break
        
    print(f"Usted esta apostando ${bet} a {lines} lineas. \nSu apuesta total es de ${total_bet}.")
    
    slots = get_slot_machine_spin(ROWS, COLUMNS, symbol_count)
    print_slot_machine(slots)
    winnings, winning_lines = check_winnings(slots, lines, bet, symbol_value)
    print(f"Usted gano ${winnings}.")
    print(f"Usted gano en las lineas:", *winning_lines)
    return winnings - total_bet

def main():
    balance = deposit()
    while True:
        if balance > 0:
            print(f"Su balance actual es ${balance}")
            answer = input("Presione Enter para jugar o Q para salir: ")
            if answer.lower() == "q":
                break
            balance += spin(balance)
        else:
            break
        
    print(f"Usted se retira con ${balance}")
    
    
main()
    