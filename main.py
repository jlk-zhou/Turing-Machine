from helper import *
import sys

try:
    # Load user's input onto an initialised machine
    machine = load(sys.argv)

    # Get expression from commandline
    expression = interpret(sys.argv)

# If user doesn't know the correct usage
except IndexError:
    print("Usage: python main.py operation argument1 [argument2] ... ")
    sys.exit()

# Print initial interface
print(f"Your expression: {expression}")
print_machine(machine, "start")
input("Press Enter to start! ")

# Carry out animation for user's chosen operation
machine = turing(machine)

# Compute the output according to the machine's final stage
out = output(machine)
print(f"{expression} = {out}")
print_machine(machine, "finish")
