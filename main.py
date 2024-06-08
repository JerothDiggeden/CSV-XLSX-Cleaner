import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui as pg
from tqdm import tqdm


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
lst = ["NONE"]
word_del = ["NONE"]
word_lst = []
count = []
new_names = []


def activate():
    # Activate PowerShell window by sending Alt+Tab key combination
    pg.hotkey('alt', 'tab')


def click():
    pg.click()


# PROMPT FOR FILE NAME
while df.empty:
    root = tk.Tk()
    root.withdraw()

    try:
        csv = messagebox.askokcancel("Import File", "Do you want to import a file?", parent=root)
        if csv:
            file = filedialog.askopenfilename(parent=root)
            click()
            if not file:
                raise FileNotFoundError
        else:
            exit()
    except FileNotFoundError:
        print(red + "NO FILE SELECTED, PLEASE SELECT A FILE!")
        continue
    # IMPORT DATA
    try:
        ext_len = len(file) - 3
        ext = file[ext_len:]
        if ext == "csv":
            df = pd.read_csv(file)
            df_new = pd.read_csv(file)
        elif ext == "lsx":
            df = pd.read_excel(file)
        elif ext == "xls":
            df = pd.read_excel(file)
    except UnicodeDecodeError:
        print(red + "WRONG FILE TYPE, PLEASE SELECT A CSV FILE!")
        continue

col_names = df.columns

# FUNCTION TO REPLACE COLUMN NAMES


def apply(del_sym, del_word):
    column_names_func = df.columns.tolist()
    print("")
    rep_sym = input(f"{green}REPLACE SYMBOL WITH? ")
    rep_wrd = input(f"{green}REPLACE WORD WITH? ")
    for rn in range(len(column_names_func)):
        # SYMBOL
        for sym_rep in range(len(del_sym)):
            # REMOVE SYMBOL FROM STRING
            column_names_func[rn] = column_names_func[rn].replace(del_sym[sym_rep], rep_sym)
        # WORD
        # SPLIT STRING INTO INDIVIDUAL WORDS
        words = column_names_func[rn].split()
        for idx, word in enumerate(words):
            # Iterate over words, not indices
            if word in del_word:
                # If the word needs to be replaced, replace it
                words[idx] = rep_wrd
                words[idx] = words[idx].strip()
        # JOIN WORDS BACK INTO STRING
        new_name = " ".join(words).strip()
        new_names.append(new_name)
    # Create a dictionary mapping old column names to new column names
    column_names_dict = dict(zip(df.columns, new_names))
    df_replaced = df.rename(columns=column_names_dict)
    print("")
    print(blue + "PREVIEW OF NEW COLUMN NAMES:" + reset)
    print(yellow + f"{df_replaced.columns}" + reset)
    print("")
    save = input(blue + f"{red}(1){blue}SAVE CHANGES OR {red}(2){blue}EDIT AGAIN? " + reset)
    if save == "1":
        print("")
        print(blue + "DONE! HERE ARE THE NEW COLUMN NAMES: " + reset)
        print(df_replaced.columns)
        return df_replaced.columns
    elif save == "2":
        return True


def save():
    save = input(blue + f"{red}(1){blue}SAVE FILE OR {red}(2){blue}EDIT AGAIN? " + reset)
    if save == "1":
        # WRITE TO NEW FILE
        new_file = filedialog.asksaveasfilename(defaultextension=".csv", parent=root,
                                                filetypes=[("CSV Files", "*.csv"),
                                                           ("XLSX Files", "*.xlsx")])
        activate()
        if new_file:
            if ext == "csv":
                df.to_csv(new_file, index=False)
            elif ext == "lsx":
                df.to_excel(new_file, index=False)
            elif ext == "xls":
                df.to_excel(new_file, index=False)
    elif save == "2":
        return True


def true_false():
    # Calculate the total number of iterations (cells) in the DataFrame
    total_iterations = df.size

    # Initialize the progress bar
    with tqdm(total=total_iterations) as pbar:
        # Iterate over each cell in the DataFrame
        for index, value in df.stack().items():
            # Perform your processing here
            if value == 'Yes':
                df.at[index] = 'TRUE'
            elif value == 'No':
                df.at[index] = 'FALSE'

            # Update the progress bar
            pbar.update(1)


def nan(df_new):
    # Calculate the total number of iterations (cells) in the DataFrame
    df_new = df_new.dropna()

    return df_new  # Return the modified DataFrame


if __name__ == "__main__":

    while True:
        for i in lst:
            print(blue + """ 
                      @@@@@@@@@@   @@@@@@@@@  @@@@@@@@@@@      @@@     @@@@@@@@           @@@  @@@@@@@@@@@       @@  
                    @@   @@@@@   @@@@     @  @   @@@   @     @@@@     @@@   @@@@        @@@   @   @@@   @     @@@@  
                        @@@@     @@@   @        @@@@       @@@@@     @@@@   @@@@      @@@@@      @@@@        @@@@@  
                      @@@@@     @@@@ @@@        @@@       @  @@@     @@@    @@@@     @  @@@      @@@       @@ @@@@  
                     @@@@       @@@            @@@@     @@@@@@@@    @@@@    @@@    @@@@@@@@     @@@@     @@@@@@@@@  
                   @@@@    @@  @@@@     @     @@@@      @     @@@   @@@   @@@@   @@     @@@     @@@     @@    @@@   
                 @@@@@@@@@@@  @@@@@@@@@@@    @@@@@   @@@    @@@@@ @@@@@@@@@@   @@@@    @@@@@  @@@@@   @@@    @@@@@"""
                  + reset)
            print("")
            print("")
            column_names = df.columns.tolist()
            print(yellow + "COLUMN NAMES" + reset)
            print(column_names)
            print("")
            print(yellow + "LIST OF SYMBOLS TO REMOVE" + red)
            print(*lst)
            print("")
            print(yellow + "LIST OF WORDS TO REMOVE" + red)
            print(*word_del)
            print("" + reset)
            sel = input(f"{blue}(1){green}REMOVE SYMBOL {blue}(2){green}REMOVE WORD {blue}(3){green}APPLY CHANGES "
                        f"{blue}(4){green}EDIT LISTS {blue}(5){green}CAPITALIZE or LOWER CASE {blue}(6){green}"
                        f"TRUE & FALSE {blue}(7){green}REMOVE NAN ROWS {blue}(8){green}SAVE {blue}(9)"
                        f"{green}EXIT?" + reset)

            match sel:
                case "1":
                    lst.remove("NONE")
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
                    word_del.remove("NONE")
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
                    # Strip whitespace from elements in lst
                    lst = [item.strip() for item in lst]
                    if "NONE" in lst:
                        lst.pop(0)
                    if "NONE" in word_del:
                        word_del.pop(0)
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
                    execute = input(f"{red}(1){blue}EXECUTE OR {red}(2){blue}BACK?: " + reset)
                    match execute:
                        case "1":
                            df.columns = apply(lst, word_del)
                        case "2":
                            continue

                case "4":
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

                case "5":
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
                case "6":
                    print("")
                    t_f = input(f"{red}(1){green}CONVERT YES & NO TO TRUE & FALSE OR {red}(2){green}BACK?")
                    if t_f == "1":
                        true_false()
                    elif t_f == "2":
                        continue

                case "7":
                    print("")
                    t_f = input(f"{red}(1){green}DELETE ROWS WITH NaN CELLS OR {red}(2){green}BACK?")
                    if t_f == "1":
                        df = nan(df)
                    elif t_f == "2":
                        continue

                case "8":
                    save()

                case  "9":
                    exit()

                case _:
                    print("")
                    print(red + "INVALID INPUT, TRY AGAIN..." + reset)
                    print("")
