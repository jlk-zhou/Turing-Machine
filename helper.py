import time

"""loads users input and initialise the machine"""
def load(cml_arg):
    SIZE = 25

    # Initialise the machine
    tape = []
    position = 0
    state = 1

    # Initialize the window
    window = [0, SIZE]

    operation = cml_arg[1]

    # # Interpret inputs from user
    # x = int(math[1])
    # y = int(math[2])
    for i in range(len(cml_arg) - 2):

        # Put arguments on the tape
        for _ in range(int(cml_arg[i + 2]) + 1):
            tape.append("1")

        # There should be a zero between the two inputs
        tape.append("0")

    # # Put the second input on the tape
    # for _ in range(y + 1):
    #     tape.append("1")

    # tape.append("0")

    # Fill out the rest of the window, if needed
    if len(tape) < SIZE:
        for _ in range(SIZE - len(tape) - 1):
            tape.append("0")

    # Done! Now hand back the machine
    machine = {"tape": tape,
               "position": position,
               "state": state,
               "window": window,
               "operation": operation
               }

    return machine


"""Interpret user's commandline arguments as an expression"""
def interpret(cml_arg):
    expression = []
    expression.append(cml_arg[1] + "(")
    for i in range(len(cml_arg) - 2):
        expression.append(cml_arg[i + 2])
        expression.append(", ")
    expression.pop(-1)
    expression.append(")")

    expression = "".join(expression)

    return expression


"""Print out a Turing Machine. Given the machine and window frame,
print the machine on the screen and return nothing"""
def print_machine(m, init=None):
    if init != None:
        print("", end="")
    else:
        print("\n")

    print("..." + "".join(m["tape"][m["window"][0]:m["window"][1]]) + "...")
    print("   " + (" " * (m["position"] - m["window"][0])) + "^")
    print("   " + (" " * (m["position"] - m["window"][0])) + str(m["state"]))
    time.sleep(0.1)


"""Return the integer state of the machine, start counting from 0"""
def in_state(m):
    return m["state"] - 1


"""Make machine go to another state"""
def goto_state(m, s):
    if in_state(m) != s:
        m["state"] = s
        print_machine(m)
    return m


"""Return the integer position the machine is currently scanning"""
def position(m):
    return m["position"]


"""Return the character machine's scanning at current position"""
def scanning(m):
    return m["tape"][position(m)]


"""Run script, which is a set of quadruples, that define a turing machine"""
def run(m, script):
    while True:

        # Hash to the line of the script corresponding to the current state
        try:
            overt = script[in_state(m)][scanning(m)][0]
            covert = script[in_state(m)][scanning(m)][1]
        except IndexError:
            return m

        if overt == "R":
            m = right(m)
        elif overt == "L":
            m = left(m)
        elif overt == "1":
            m = replace(m, "1")
        elif overt == "0":
            m = replace(m, "0")

        m = goto_state(m, covert)


"""Convert the final stage of a machine into an integer"""
def output(m):
    out = -1
    for bit in m["tape"]:
        if bit == "1":
            out += 1
    return out


"""Make machine go right one block"""
def right(m):
    m["position"] += 1

    # If the cursor isn't out of the window
    if m["position"] < m["window"][1]:
        print_machine(m)

    # If the cursor went out of the window
    else:

        # Did the machine go off the tape?
        if m["position"] >= len(m["tape"]):

            # Extend the tape to the right by one bit
            m["tape"].append("0")

        # Move the window frame towards the right by one bit
        for i in range(len(m["window"])):
            m["window"][i] += 1

        print_machine(m)

    return m


"""Make machine go left one block"""
def left(m):
    m["position"] -= 1

    # Given that the cursor isn't out of the window
    if m["position"] >= m["window"][0]:
        print_machine(m)

    # If the cursor went out of the window
    else:

        # If the cursor went off the tape
        if m["position"] < 0:

            # Extend the tape towards the left by one bit
            m["tape"].insert(0, "0")
            m["position"] = 0

        else:
            # Move the entire window frame one bit towards the left
            for i in range(len(m["window"])):
                m["window"][i] -= 1

        print_machine(m)

    return m


"""Replace the character the machine's currently scanning"""
def replace(m, bit):
    if scanning(m) != bit:
        animation = ["_", bit]
        for frame in animation:
            m["tape"][position(m)] = frame
            print_machine(m)
    return m


"""Compile Turing Machine script from a text file into the code"""
def compile(operation):
    script = []
    filename = operation + ".txt"
    with open(filename, "r") as file:

        # Iterate over the lines that represents a state
        for line in file:

            # Replace each B with 0
            line = line.replace("B", "0")

            # If the machine knows what to do for both possible scanning bits
            if "," in line:

                # Give proper structure for this case
                script.append({"1": (line[5], int(line[8])), "0": (line[16], int(line[19]))})

            # If we only told machine what to do if it scanned one bit
            else:
                script.append({line[3]: (line[5], int(line[8]))})

    return script


"""A function that carries out calculation, animated Turing machine style"""
def turing(m):
    script = compile(m["operation"])
    m = run(m, script)
    return m
