import math
import json
from pathlib import Path

def get_desktop_path():
    desktop = Path.home() / "Desktop"
    # Go to the home folder if there's no Desktop folder
    return desktop if desktop.is_dir() else Path.home()

RESULT_FILE = get_desktop_path() / "last_result.json"

def save_result(value):
    try:
        RESULT_FILE.write_text(json.dumps({"result": value}))
        return True
    except OSError as e:
        print(f"Could not save result: {e}")
        return False

def load_result():
    try:
        return float(json.loads(RESULT_FILE.read_text())["result"])
    except (OSError, ValueError, KeyError, json.JSONDecodeError):
        return None

COLOR = "\033[38;2;86;169;182m"
RESET = "\033[0m"

def get_number(prompt):
    constants = {'pi': math.pi, 'e': math.e, 'tau': math.tau}
    while True:
        value = input(prompt).strip().lower()
        if value in constants:
            return constants[value]
        if value in ('ans', 'last'):
            saved = load_result()
            if saved is None:
                print("No saved results")
                continue
            return saved
        try:
            number = float(value)
            if math.isfinite(number):
                return number
            break
        except ValueError:
            pass
        print("Invalid input; enter a number in standard or e-notation, a constant (pi, e, tau), or 'ans' for your last saved result")

def remove_trailing(x):
    # Show whole numbers without the trailing 0
    return str(int(x)) if x.is_integer() else str(x)

def main():
    print("Welcome to my command line calculator\n" + "-" * 17)
    num1 = get_number("Enter the first number: ")
    num2 = get_number("Enter the second number: ")

    valid_operators = ['+', '-', '*', '/', '^', '**', '//', '%']
    print("Choose an operator:\n", *valid_operators)

    while True:
        operator = input("Select an operator: ").strip()
        if operator in valid_operators:
            break
        print("Invalid operator; enter only the symbol ('+') and not the name ('addition')")

    # mode is 'decimal', 'whole', 'auto' (to format automatically), or None (for // and %, which aren't rounded)
    mode = None
    if operator in ['+', '-', '*', '/', '^', '**']:
        while mode is None:
            choice = input("\nDo you want the output in decimals or whole numbers? "
                           "Type 'a' to format automatically [d/w/a]: ").strip().lower()
            if choice in ['d', 'decimal']:
                mode = 'decimal'
            elif choice in ['w', 'whole']:
                mode = 'whole'
            elif choice in ['a', 'auto', 'automatic', 'automatically']:
                mode = 'auto'
            else:
                print("Enter 'd' for decimals, 'w' for whole numbers, or 'a' for auto")

    decimals = 2
    want_remainder = False

    if mode == 'decimal':
        while True:
            try:
                decimals = int(input("Enter amount of decimal places: "))
                if decimals >= 0:
                    break
                print("Decimal places can't be negative")
            except ValueError:
                print("Enter a whole number")
    elif mode == 'whole' and operator == '/':
        want_remainder = input("Do you want to calculate the remainder? [y/n]: ").strip().lower() in ['y', 'yes']

    # Calculate
    try:
        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator in ('^', '**'):
            result = num1 ** num2
        elif operator == '/':
            result = num1 / num2
        elif operator == '//':
            result = num1 // num2
        else:  # '%'
            result = num1 % num2
    except ZeroDivisionError:
        print("\nMATH ERROR: Cannot divide by 0; raising 0 to a negative power also causes this")
        return
    except OverflowError:
        print("\nOVERFLOW ERROR: Result too large")
        return
    if isinstance(result, complex):
        print("\nMATH ERROR: Result is not a real number")
        return
    if not math.isfinite(result):
        print("\nOVERFLOW ERROR: Result too large")
        return
    if want_remainder:
        quotient = num1 // num2
        remainder = num1 % num2
        print(f"> Calculation: {COLOR}{remove_trailing(num1)} / {remove_trailing(num2)} = {remove_trailing(quotient)} R {remove_trailing(remainder)}{RESET}") # Print the result with the remainder
        return
    if mode == 'whole':
        result_str = str(round(result))
    elif mode == 'decimal':
        result_str = f"{result:.{decimals}f}"
    else:  # If the mode auto or the operation is // or %
        result_str = remove_trailing(result)

    print(f"> Calculation: {COLOR}{remove_trailing(num1)} {operator} {remove_trailing(num2)} = {result_str}{RESET}") # Print the result normally

    # Save result
    if input("\nSave this result for later use? [y/n]: ").strip().lower() in ['y', 'yes']:
        if save_result(result):
            print("Saved to desktop if possible, otherwise saved to home folder; type 'ans' at a number prompt to use it\n\n")

main()
