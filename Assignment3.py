'''
Summary of the program: Program prompts the user to pick a file folder. Then it will scan the folder for .txt files and
iterates through them to compare the text files to one another.After this, it uses Jaccard Similarity to compare the
file's similarity using the set of words that is representing each file, which is not including any stop words that is
probably filtered out.Lastly, the files of highest similarity are printed out in Tkinter in a tabular form.
'''
import tkinter as tk
import glob
import os
from tkinter.filedialog import askdirectory

# Initializes a all the variables to be used globally
highest_sim_list = []
highest_sim_dict = {}
current_file_list = []
stop_words_list = []
text_file_dict1 = {}
text_file_dict2 = {}
text_file_set = set()
text_file_set2 = set()

# Load stop words from stop words file
stop_words = open("C:\\Users\\jayan\\OneDrive\\Desktop\\Stopwords.txt").read()

# Appends the stop words to a new list
with open("C:\\Users\\jayan\\OneDrive\\Desktop\\Stopwords.txt") as Stopwords:
    for line in Stopwords:
        word = line.strip()
        stop_words_list.append(word)

# Allow user to choose the directory for the text files and then accesses them
text_directory = askdirectory \
    (initialdir="C:\\Users\\jayan\\OneDrive\\Desktop\\Cisc121_Assignment3_texts")
text_files = glob.glob(text_directory + "/" + "*.txt")

# Makes a new list with all of the file names to be used later
for file in text_files:
    current_file_list.append(file)


def process_text():
    '''
    Parameters:
        none
    Returns:
        none

    Description:
        This function takes each text file, reads it word by word,
        puts every word that is not a stop word into a set,
        and then compares each text file with every other text file.
        It will do this for every text file in order.
        Once the file we are comparing is compared with another,
        it will calculate the similarity using the Jaccard Simlarity meassure.
        Then, it records the highest similarity meassure,
        and adds the name of the file, the file most similar to it,
        and the similarity meassure into a dictionary to be printed in tkinter later.

        Since we don't know how many files the user want to process,
        the amount of loops will be equal to the amount of files squared
        so that every file is compared to every file.
    '''

    highest_sim = 0
    high_sim_name = ""
    cur_file_num = 0
    list_index = 0
    similarity = 0
    compare_num = 0

    loop_times = len(current_file_list) ** 2

    for loops in range(loop_times):

        if compare_num == len(current_file_list):
            '''
            This if statement will only run at the end of a "comparison loop".
            For example: if we have compared file one to EVERY other file, 
            this if statement will run to keep track of the file with the highest similarity. 
            This statement will add the file that is most similar 
            and the value of that similarity to a list,
            then it will add those elements of the list to a dictionary as the values of the key
            that is equal to the file we are comparing. 
            '''
            cur_file_num = cur_file_num + 1
            compare_num = 0
            highest_sim_list.extend([high_sim_name, highest_sim])
            highest_sim_dict[cur_file_name.split(" ")[0]] = highest_sim_list[list_index:list_index + 2]
            highest_sim = 0
            similarity = 0
            intersection = 0
            union = 0
            high_sim_name = ""
            list_index = list_index + 2


        current_file = open(current_file_list[cur_file_num], encoding="utf8")
        compare_file = open(current_file_list[compare_num], encoding="utf8")
        text_in_file = list(current_file.read().split())
        text_in_file2 = list(compare_file.read().split())
        cur_file_name = os.path.basename(str(current_file))
        com_file_name = os.path.basename(str(compare_file))

        for word in text_in_file:
            if word not in stop_words_list:
                if word in text_file_dict1:
                    text_file_dict1[word] += 1
                else:
                    text_file_dict1[word] = 1

                if text_file_dict1[word] > 4:
                    text_file_set.add(word)

        for word in text_in_file2:
            if word not in stop_words_list:
                if word in text_file_dict2:
                    text_file_dict2[word] += 1
                else:
                    text_file_dict2[word] = 1

                if text_file_dict2[word] > 4:
                    text_file_set2.add(word)

        # Next three lines are the Jaccard similarity measure.
        intersection = text_file_set.intersection(text_file_set2)
        union = text_file_set.union(text_file_set2)
        similarity = len(intersection) / len(union)

        if similarity > highest_sim and similarity < 1:
            # Keeping track of which file has the highest similarty
            highest_sim = similarity
            high_sim_name = com_file_name.split(" ")[0]

        # Clears the sets and dictionaries so that the words don't pile up each loop.
        text_file_set.clear()
        text_file_set2.clear()
        text_file_dict1.clear()
        text_file_dict2.clear()
        compare_num = compare_num + 1
        loops = loops + 1

        if loops == loop_times:
            '''
            This if statement is the same as the one at the 
            top of the function, but is placed down here so that the 
            last file will still be processed. 
            '''
            cur_file_num = cur_file_num + 1
            compare_num = 0
            highest_sim_list.extend([high_sim_name, highest_sim])
            highest_sim_dict[cur_file_name.split(" ")[0]] = highest_sim_list[list_index:list_index + 2]
            highest_sim = 0
            similarity = 0
            intersection = 0
            union = 0
            high_sim_name = ""
            list_index = list_index + 2

        similarity = 0
        intersection = 0
        union = 0


process_text()

# Prints the results in tkinter.
# The lines up to the for loop initilize
# The grid that will be dislpayed with headers.
window = tk.Tk()
window.geometry("1200x800")

key_list = []
col0_header = tk.Label(window, text="text", pady=10)
col0_header.grid(row=0, column=0)

col1_header = tk.Label(window, text="text with highest similarity, and the similarity value", pady=10)
col1_header.grid(row=0, column=1)

rows = len(current_file_list)
columns = 3

for key in highest_sim_dict.keys():
    key_list.append(key)

for row in range(rows):
    # Line one prints out the file beling processed.
    # Line two prints out the file most similar to it, and the value of that similarity.
    tk.Label(window, text=key_list[row]).grid(row=row + 1, column=0)
    tk.Label(window, text=highest_sim_dict[key_list[row]]).grid(row=row + 1, column=1)

window.mainloop()
