import os
import random

try:
    from colorama import Fore, Style, init
    COLOR = True
except:
    COLOR = False

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
        print("%02d: %s" % (i, file))
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


def colorWord(word, restOfColor: str = None):
    word = str(word).strip()

    if not COLOR:
        return word
    splitword = word.split(" ")

    if restOfColor == "red":
        restOfColor = Fore.RED
    elif restOfColor == "green":
        restOfColor = Fore.GREEN
    elif restOfColor == "blue":
        restOfColor = Fore.BLUE

    if len(splitword) == 2:
        if splitword[0] == "der":
            splitword[0] = Fore.BLUE + "der" + Fore.RESET
        elif splitword[0] == "die":
            splitword[0] = Fore.RED + "die" + Fore.RESET
        elif splitword[0] == "das":
            splitword[0] = Fore.GREEN + "das" + Fore.RESET
        else:
            if restOfColor is not None:
                return restOfColor + word
            else:
                return word
        if restOfColor is not None:
            word = splitword[0] + " " + restOfColor + splitword[1] + Fore.RESET
        else:
            word = splitword[0] + " " + splitword[1]
    else:
        if restOfColor is not None:
            word = restOfColor + word

    return word


def askWord(wordAsked, wordSK: str):
    global filename

    if COLOR:
        answer = input(Fore.CYAN + wordSK + Fore.RESET + ": ").strip()
    else:
        answer = input(wordSK + ": ").strip()

    if answer == "exit":
        close()
    elif answer == "save":
        saveCorrectWords(filename + ".cor")
        return 0

    if answer == wordAsked:
        if COLOR:
            print(Fore.GREEN + "Good, " + colorWord(wordAsked, "green"))
        else:
            print("Good, " + colorWord(wordAsked))
        return 1
    else:
        answerSplit = answer.split(" ")
        wordSplit = wordAsked.split(" ")
        points = 0

        for i in range(len(answerSplit)):
            if i >= len(wordSplit):
                points = 0
                break
            if answerSplit[i] == wordSplit[i]:
                points -= 1 / len(answerSplit)

        if points == 0:
            points = -1
        if COLOR:
            print(Fore.RED + "Wrong", ", correct: ", Fore.CYAN + wordSK, " = ",
                  colorWord(wordAsked, "red"), sep="")
        else:
            print("Wrong", ", correct: ", wordSK, " = ", wordAsked, sep="")
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


def spaceAlignColored(text, orgText, numofSpaces):
    strtext = str(orgText)
    numofSpaces -= len(strtext)
    if numofSpaces > 0:
        return text + (" " * numofSpaces)
    return text


def printAllWords():
    global slova, correct
    y = 0
    i = 0
    for wordpair in slova:
        print(
            "SKIP: ",
            spaceAlign(wordpair[0], 7),
            "DE: ",
            spaceAlignColored(colorWord(wordpair[1]), wordpair[1], 35),
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
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def enterToContinue():
    input("Press Enter to continue")


clear()

if not COLOR:
    print("You don't have \"colorama\" installed, text colors won't work\n")
else:
    init(autoreset=True)

filename = getFileName()

readFileToDB(filename)

for i in range(0, len(slova)):
    correct.append(0)

readCorrectWords(filename + ".cor")

if yesOrNoInput("Print table of all words? "):
    print()
    printAllWords()
    enterToContinue()


def main():
    clear()

    print("Select mode:")
    print("1 - Normal practice mode")
    print("2 - Learning mode (5 rotating words)")
    mode = input("Choice: ")

    if mode == "2":
        learning_mode()
    else:
        normal_mode()


def normal_mode():
    numCorrect = 0
    correctNumMax = 4

    numberOfCorrectWords = 0
    numberOfWords = 0
    correctInRow = 0

    while True:
        unknownWords = []

        for i in range(0, len(slova)):
            if correct[i] >= 2 or slova[i][0]:
                numCorrect += 1
                continue

            numberOfWords += 1
            print(f"{i + 1}/{len(slova) + 1} ", end="")
            correctNow = askWord(slova[i][1], slova[i][2])
            correct[i] += correctNow
            if correctNow == 1:
                numberOfCorrectWords += 1
                correctInRow += 1
            else:
                correctInRow = 0
            if correctInRow > 2:
                if COLOR:
                    print(Fore.GREEN + "Correct in a row: " + str(correctInRow))
                else:
                    print("Correct in a row: " + str(correctInRow))

        for unknownWord in unknownWords:
            askWord(unknownWord[1], unknownWord[2])

        if numCorrect == len(slova):
            if COLOR:
                print(Fore.GREEN + "Good job, you know everything")
            else:
                print("Good job, you know everything")
            enterToContinue()
            close()

        print("You know %i%% of the words" %
              (int(numberOfCorrectWords / numberOfWords * 100)))

        numCorrect = 0

        enterToContinue()
        clear()


def learning_mode():
    """
    Learning mode: keep 5 active words, ask them repeatedly in random order.
    When a word reaches correctNumMax (4) it is replaced by the next unlearned word.
    If we run out of new words we wrap to the beginning.
    After each full pass over the 5 active words the screen is cleared.
    """
    correctNumMax = 4
    n = len(slova)
    if n == 0:
        print("No words available.")
        return

    learned = [0] * n
    active_size = 5
    active_words = [i % n for i in range(active_size)]
    next_word_pointer = active_size % n

    def find_next_candidate(start):
        idx = start % n
        for _ in range(n):
            if idx not in active_words and learned[idx] < correctNumMax:
                return idx
            idx = (idx + 1) % n
        return None

    while True:
        # Check if all words are learned
        if all(c >= correctNumMax for c in learned):
            if COLOR:
                print(Fore.GREEN + "Great job! You've learned all the words.")
            else:
                print("Great job! You've learned all the words.")
            enterToContinue()
            close()

        # Shuffle the order for this round
        round_order = active_words.copy()
        random.shuffle(round_order)

        for word_idx in round_order:
            # if this slot points to a mastered word, try replacing it
            if learned[word_idx] >= correctNumMax:
                candidate = find_next_candidate(next_word_pointer)
                if candidate is not None:
                    active_words[active_words.index(word_idx)] = candidate
                    next_word_pointer = (candidate + 1) % n
                    word_idx = candidate
                else:
                    continue  # all learned or no candidate left

            correctNow = askWord(slova[word_idx][1], slova[word_idx][2])
            if correctNow == 1:
                learned[word_idx] += 1
            else:
                learned[word_idx] = max(0, learned[word_idx] - 0)

            # Replace mastered word immediately
            if learned[word_idx] >= correctNumMax:
                candidate = find_next_candidate(next_word_pointer)
                if candidate is not None:
                    active_words[active_words.index(word_idx)] = candidate
                    next_word_pointer = (candidate + 1) % n

        # End of a full pass
        if COLOR:
            print(Fore.CYAN + "\nRound complete.")
        else:
            print("\nRound complete.")

        enterToContinue()
        clear()


main()
