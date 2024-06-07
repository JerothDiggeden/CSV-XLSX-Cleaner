import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os


def main():
    # COLOURS
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    reset = '\033[0m'  # Reset text color to default

    # VARIABLES
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    df = pd.DataFrame
    file = ""
    lst = [""]
    symbols_lst = []
    word_lst = []
    word_del = [""]
    count = []

    # PROMPT FOR FILE NAME
    while df.empty:
        try:
            file = filedialog.askopenfilename()
            if not file:
                raise FileNotFoundError
        except FileNotFoundError:
            print(red + "NO FILE SELECTED, PLEASE SELECT A FILE!")
            continue
        # IMPORT DATA
        try:
            df = pd.read_csv(file)
        except UnicodeDecodeError:
            print(red + "WRONG FILE TYPE, PLEASE SELECT A CSV FILE!")
            continue

    col_names = df.columns

    # FUNCTION TO REPLACE COLUMN NAMES

    def rename(del_sym, del_word):

        column_names_func = df.columns.tolist()
        print("")
        rep_sym = input(f"{green}REPLACE SYMBOL WITH? ")
        rep_wrd = input(f"{green}REPLACE WORD WITH? ")
        for c in range(len(column_names_func)):
            # SYMBOL
            for sym_rep in range(len(del_sym)):
                # REMOVE SYMBOL FROM STRING
                column_names_func[c] = column_names_func[c].replace(del_sym[sym_rep], rep_sym)
            # WORD
            # SPLIT STRING INTO INDIVIDUAL WORDS
            words = column_names_func[c].split()
            for wrd_rep in range(len(del_word)):
                # REMOVE WORD FROM LIST
                try:
                    words.remove(del_word[wrd_rep])
                except ValueError:
                    continue
            # JOIN WORDS BACK INTO STRING
            column_names_func[c] = " ".join(words)

        # WRITE TO NEW FILE
        df.columns = column_names_func
        new = input("ENTER A FILE NAME: ")
        new_file = os.path.dirname(file)
        print(new_file)
        df.to_csv(f"{new_file}/{new}.csv", index=False)
        print("")
        print(blue + "DONE! HERE ARE THE NEW COLUMN NAMES: " + reset)
        print(df.columns)
        lst.clear()
        word_del.clear()
        exit()

    while True:
        for i in lst:
            column_names = df.columns.tolist()
            print(yellow + "COLUMN NAMES" + reset)
            print(column_names)
            print("")
            print(yellow + "LIST OF SYMBOLS TO REMOVE" + reset)
            print(*lst)
            print("")
            print(yellow + "LIST OF WORDS TO REMOVE" + reset)
            print(*word_del)
            print("")
            sel = input(f"{blue}(1){green}REMOVE SYMBOL, {blue}(2){green}REMOVE WORD, {blue}(3){green}EDIT LISTS, "
                        f"{blue}(4){green}CAPITALIZE or LOWER CASE, {blue}(5){green}COMMIT & REMOVE, {blue}(6)"
                        f"{green}EXIT? " + reset)

            match sel:
                case "1":
                    print("")
                    resp = input(green + "ENTER SYMBOL/S TO REMOVE: " + reset)
                    if len(resp) == 1:
                        try:
                            lst.append(resp)
                            count.append(0)
                            print("")
                            print(blue + f"{resp} ADDED TO LIST" + reset)
                            print("")
                        except ValueError:
                            continue
                    elif len(resp) < 1:
                        print(red + "NO SYMBOL DETECTED, TRY AGAIN..." + reset)
                        continue
                    elif len(resp) > 1:
                        lst1 = list(resp)
                        for s in lst1:
                            lst.append(s)
                        print("")
                        print(blue + f"{resp} ADDED TO LIST" + reset)
                        print("")

                case "2":
                    print("")
                    word = input(green + "ENTER A WORD/S TO REMOVE: " + reset)
                    if "1" in word or "2" in word or "3" in word or "4" in word or "5" in word or "6" in word or "7" in word or "8" in word or "9" in word or "0" in word:
                        print(red + "INVALID INPUT, PLEASE ENTER LETTERS OR WORDS!")
                        continue
                    if word == "":
                        print(red + "INVALID INPUT, PLEASE ENTER LETTERS OR WORDS!")
                        continue
                    if " " in word:
                        word_del = word.split()
                    elif " " not in word:
                        word_del.append(word)
                    if len(word_lst) == 1:
                        try:
                            word_del.append(word)
                            print("")
                            print(blue + f"{word} ADDED TO LIST" + reset)
                            print("")
                        except ValueError:
                            continue
                    elif len(word_del) > 1:
                        try:
                            for word_n in word_lst:
                                word_del.append(word_n)
                            print("")
                            print(blue + f"{word} ADDED TO LIST" + reset)
                            print("")
                        except ValueError:
                            continue

                case "3":
                    print("")
                    sw = input(f"{green}EDIT {blue}(1){green}SYMBOL OR {blue}(2){green}WORD LIST?: " + reset)
                    match sw:
                        case "1":
                            print("")
                            print(yellow + "SYMBOL LIST TO EDIT:" + reset)
                            print("")
                            print(*lst)
                            print("")
                            edit_s = input(green + "ENTER SYMBOL/S TO DELETE: " + reset)
                            if len(edit_s) == 1:
                                lst.remove(edit_s)
                                print("")
                                print(red + f"{edit_s} REMOVED FROM LIST" + reset)
                                print("")
                            elif len(edit_s) > 1:
                                for e in lst:
                                    if e in lst:
                                        lst.remove(e)
                                print("")
                                print(red + f"{edit_s} REMOVED FROM LIST" + reset)
                                print("")
                        case "2":
                            print("")
                            print(yellow + "WORD LIST TO EDIT:" + reset)
                            print("")
                            print(*word_del)
                            print("")
                            edit_w = input(green + "ENTER WORD/S TO DELETE: " + reset)
                            if edit_w in word_del:
                                word_del.remove(edit_w)
                                print("")
                                print(red + f"{edit_w} DELETED FROM WORD LIST:" + reset)
                                print("")
                            else:
                                print("")
                                print(red + "WORD NOT FOUND IN LIST, TRY AGAIN...:" + reset)
                                print("")

                case "4":
                    cap = input(f"{blue}(1){green}CAP ALL, {blue}(2){green}CAP FIRST or "
                                f"{blue}(3){green}LOWER ALL? " + reset)
                    match cap:
                        case "1":
                            for c in column_names:
                                column_names[column_names.index(c)] = c.upper()
                                lst = [item.upper() for item in lst]
                                word_del = [item.upper() for item in word_del]
                            df.columns = column_names
                        case "2":
                            for c in column_names:
                                column_names[column_names.index(c)] = c.title()
                                lst = [item.title() for item in lst]
                                word_del = [item.title() for item in word_del]
                            df.columns = column_names
                        case "3":
                            for c in column_names:
                                column_names[column_names.index(c)] = c.lower()
                                lst = [item.lower() for item in lst]
                                word_del = [item.lower() for item in word_del]
                            df.columns = column_names

                case "5":

                    lst.remove("")
                    # Strip whitespace from elements in lst
                    lst = [item.strip() for item in lst]
                    print("")
                    print(f"{red}TO BE REMOVED:")
                    print("")
                    print(f"SYMBOLS: {lst}")

                    # Strip whitespace from elements in word_del
                    if "" in word_del:
                        word_del.remove("")
                    else:
                        word_del = [item.strip() for item in word_del]
                    print(F"WORDS: {word_del}")
                    print("")
                    execute = input(f"{blue}(1){red}EXECUTE OR {blue}(2){red}BACK?: " + reset)
                    match execute:
                        case "1":
                            rename(lst, word_del)
                        case "2":
                            continue

                    # Call rename function with updated lst and word_del

                case  "6":
                    exit()

                case _:
                    print("")
                    print(red + "INVALID INPUT, TRY AGAIN..." + reset)
                    print("")


if __name__ == "__main__":
    main()
