import numpy as np
import os
import random as rd

if __name__ == "__main__":
    list_of_let_and_sym = ["a", "ą", "b", "c", "ć", "d", "e", "ę", "f", "g", "h",
                           "i", "j", "k", "l", "ł", "m", "n", "ń", "o", "ó", "p",
                           "q", "r", "s", "ś", "t", "w", "u", "x", "y", "z", "ź",
                           "ż", " ", ",", "."]
    list_len = len(list_of_let_and_sym)
    dict_of_syms = {sym: i for sym, i in zip(list_of_let_and_sym, range(list_len))}

    matrix_of_freq = np.zeros((list_len, list_len), dtype=np.int64)

    folderpath = r"D:\MyOwnThings\Python_Projects\Markov_Chains_Simulates_Language\english_base"
    filepaths = [os.path.join(folderpath, name) for name in os.listdir(folderpath)]
    all_files = []

    for path in filepaths:
        with open(path, 'r', encoding='utf-8') as f:
            file = f.readlines()
            all_files.append(file)

    memory1 = None

    for text_file in all_files:
        for row in text_file:
            if row != "\n":
                for j in range(len(row)-1):
                    if j == 0 and memory1 == " ":
                        if row[j].lower() in dict_of_syms.keys() and row[j+1].lower() in dict_of_syms.keys():
                            matrix_of_freq[dict_of_syms[row[j].lower()], dict_of_syms[row[j+1].lower()]] += 1
                        if row[j].lower() in dict_of_syms.keys():
                            matrix_of_freq[dict_of_syms[" "], dict_of_syms[row[j].lower()]] += 1
                        memory = None
                    else:
                        if row[j].lower() in dict_of_syms.keys() and row[j+1].lower() in dict_of_syms.keys():
                            matrix_of_freq[dict_of_syms[row[j].lower()], dict_of_syms[row[j+1].lower()]] += 1
                        elif row[j+1] == "\n":
                            if row[j] == " ":
                                if row[j-1] == ".":
                                    matrix_of_freq[dict_of_syms["."], dict_of_syms[" "]] += 1
                                    memory1 = " "
                            elif row[j] == ".":
                                matrix_of_freq[dict_of_syms["."], dict_of_syms[" "]] += 1
                                memory1 = " "
                        else:
                            memory1 = " "

    matrix_of_probs = np.zeros((list_len, list_len))
    for i in range(list_len):
        if np.sum(matrix_of_freq[i, :]) == 0:
            matrix_of_probs[i, :] = np.zeros((1, list_len))
        else:
            matrix_of_probs[i, :] = matrix_of_freq[i, :] / np.sum(matrix_of_freq[i, :])

    dict_of_probs = {}
    i = 0
    for sym in dict_of_syms.keys():
        dict_of_probs[sym] = matrix_of_probs[i, :]
        i += 1

    print(dict_of_probs)

    x0 = "s"
    book = []
    for i in range(100):
        if i == 0:
            row = x0
        row = ""
        for j in range(30):
            x_next = rd.choices(population=list_of_let_and_sym, weights=dict_of_probs[x0], k=1)
            if j == 0:
                row += x_next[0].upper()
            else:
                row += x_next[0]
            x0 = x_next[0]
        row += "\n"
        book.append(row)

    print(book)

    with open("file.txt", "w", encoding='utf-8') as output:
        for row in book:
            output.write(row)

