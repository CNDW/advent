import os

FILE = os.path.join(os.path.dirname(__file__), 'input.txt')


with open(FILE, "r") as file:
    calories = 0
    mostest = 0
    for line in file.readlines():
        line = line.strip()
        if line == "":
            print(calories)
            if calories > mostest:
                mostest = calories
            calories = 0
        else:
            calories += int(line)

    print("MOSTEST: ", mostest)

