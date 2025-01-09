import os
from termcolor import colored

slova = []
correct = []
filename = ""


def saveCorrectWords(filename):
    f = open(filename, "w")
    for i in correct:
        f.write(str(i) + "\n")


def readCorrectWords(filename):
    if not os.path.isfile(filename):
        return
    f = open(filename, "r")
    for i in range(len(slova)):
        correct[i] = float(f.readline())


def close():
    saveCorrectWords(filename + ".cor")
    exit()


def getFileName():
    files = os.listdir()
    selFiles = []
    for file in files:
        if file.endswith(".txt"):
            selFiles.append(file)

    i = 0
    for file in selFiles:
        print(i, ": ", file)
        i += 1
    return selFiles[int(input("Zadajte cislo suboru: "))]


def readFileToDB(filename):
    global slova
    f = open(filename, "r")
    line = f.readline()
    while line != "":
        line = line.replace("\n", "")

        split = line.split(";")
        slova.append(
            [line.startswith("/"), split[0].replace("/", ""), split[1]])

        line = f.readline()


def colorWord(word):
    word = str(word).strip()

    if word.startswith("der"):
        word.replace("der", colored("der", "blue"), 1)
    elif word.startswith("die"):
        word.replace("die", colored("die", "red"), 1)
    elif word.startswith("das"):
        word.replace("das", colored("das", "green"), 1)

    return word


def colorWordColored(word, color):
    return colorWord(colored(word, color))


def askWord(wordAsked, wordSK):
    global filename

    answer = input(str(wordSK + ": "))
    if answer == "exit":
        close()
    elif answer == "save":
        saveCorrectWords(filename + ".cor")
        return 0

    if answer == wordAsked:
        print(colored("Good", "green"))
        return 1
    else:
        answerSplit = answer.split(" ")
        wordSplit = wordAsked.split(" ")
        points = 0

        for i in range(len(answerSplit)):
            if answerSplit[i] == wordSplit[i]:
                points += 1 / len(answerSplit)

        if points == 0:
            points = -1

        print(colored("Wrong", "red"), ", correct: ",
              colorWordColored(wordAsked, "red"), sep="")
        return points


def askWordDB(id):
    global slova
    return askWord(slova[id][1], slova[id][2])


def spaceAlign(text, numofSpaces):
    strtext = str(text)
    numofSpaces -= len(strtext)
    if numofSpaces > 0:
        return strtext + (" " * numofSpaces)
    return strtext


def printAllWords():
    global slova, correct
    y = 0
    i = 0
    for wordpair in slova:
        print(
            "SKIP: ",
            spaceAlign(wordpair[0], 7),
            "DE: ",
            spaceAlign(colorWord(wordpair[1]), 35),
            "SK: ",
            spaceAlign(wordpair[2], 35),
            "COR: ",
            correct[i],
            sep="",
        )
        y += 1
        i += 1
        if y % 5 == 0:
            print()


def yesOrNoInput(question):
    inp = input(question).lower().strip()
    if inp.count("y") > 0:
        return True
    return False


def clear():
    os.system("clear")


def enterToContinue():
    input("Press Enter to continue")


filename = getFileName()

readFileToDB(filename)

for i in range(0, len(slova)):
    correct.append(0)

readCorrectWords(filename + ".cor")

if yesOrNoInput("Print table of all words? "):
    print()
    printAllWords()
    enterToContinue()

clear()

numCorrect = 0

while True:
    for i in range(0, len(slova)):
        if correct[i] >= 3 or slova[i][0]:
            numCorrect += 1
            continue

        correct[i] += askWordDB(i)

        if correct[i] < -2:
            correct[i] = -2

    if numCorrect == len(slova):
        print(colored("Good job, you know everything", "green"))
        enterToContinue()
        close()

    numCorrect = 0

    enterToContinue()
    clear()
