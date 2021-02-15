import pathlib
from pathlib import Path

"""
The function split() split the users input into two part: the first letter and
the text after the first space 
"""
def split() -> list:
    user_input = input()
    types, text = user_input.strip().split(" ", 1)
    return [types, text]

"""
The function readline() reads the second input line from the user without printing any prompt, and return a type string 
(A, N, E, T) and a filter string (None if the type is A) or a type string (>, <) and a integer string (represent bytes) 
based on the input. It will loop until the user enter a correct format of input. A correct format is: a letter A by itself, or 
one of the other three types(N, E, T) followed by a space and followed by a text, or the other two types(>, <) followed 
by a space and followed by a non-zero integer. If the user enter an incorrect format of input, it will also printout 
ERROR to indicate that the input is in wrong format. 
"""

def readline() -> (str, str) or (str, int):
    while True:
        user_input = input().lstrip()
        types = user_input[0:1]
        if len(user_input) == 1 and types == "A":
            return types, None
        elif len(user_input) > 2 and (types == "N" or types == "E" or types == "T") and user_input[1] == " ":
            return types, user_input[2:]
        elif len(user_input) > 2 and (types == "<" or types == ">") and user_input[1] == " ":
            if user_input[2:].isdigit() and int(user_input[2:]) > 0:
                return types, int(user_input[2:])
        print("ERROR")

"""
The functoin read_action_line() reads the third input from the user which is the action input without printing any prompt.
It will return a type string(F, D, T) based on the input. It will loop until the user enter an input that is in correct 
format. A correct format is a string contains only one letter out of the three types(F, D, T). If the user enter in an 
incorrect format of input, the function will also print ERROR to indicate that the input is in wrong format. 
"""


def read_action_line() -> (str, int):
    while True:
        user_input = input()
        types = user_input[0:1]
        if len(user_input.strip()) == 1 and (types == "F" or types == "D" or types == "T"):
            return types
        print("ERROR")


"""
The function print_dirt2(Path) read a directory path and print all the files in it and all the subdirectories and their 
files recursively in a lexicographical order. The function works in the following ways: 

Step1, it loop through all the files and subdirectories in the given directory

Step2, it puts all the files into the file_list and sort them using sort() which automatically sort the files in 
lexicographical order. And the function also puts all the subdirectories into a directory_list and sort them in 
lexicographical order 

Step3, the function reverse the directory_list and it loops from the last directory of the list. Because we reversed the 
list, so the last one in the list would be the first one in lexicographical order. 

Step4, in the subdirectory, the function put all the files into a new temporary file list and sort then in 
lexicographical order and put all subdirectories(if any) in the subdirectory to a new temporary directory list and 
sort them in lexicographical. 

Step5, the function extent the new file list to the original file list, remove the last subdirectory on the original 
directory list and reverse the new directory list and extend it to the end of the original directory list. 

Step6, the loop will start looping and everything from step 3 to step 5 will happen again until there is no directories 
in the original directory list

After all the files are added into the file_list, they will be in lexicographical since the function sorted all the files,
directories and subdirectories step by step. 
"""


def print_dirt2(directory: Path) -> list:
    file_list = []
    dirt_list = []
    for x in Path(directory).iterdir():
        if Path(x).is_file():
            file_list.append(x)
        else:
            dirt_list.append(x)
    file_list.sort()
    dirt_list.sort()
    dirt_list = dirt_list[::-1]
    while len(dirt_list) > 0:
        sub_list1 = []
        sub_list2 = []
        index = len(dirt_list) - 1
        # I use try here to skip the directory that cannot be opened 
        try:
            for y in dirt_list[index].iterdir():
                if y.is_file():
                    sub_list1.append(y)
                else:
                    sub_list2.append(y)
        except (OSError, IOError):
            continue
        dirt_list.pop()
        sub_list1.sort()
        file_list.extend(sub_list1)
        sub_list2.sort()
        dirt_list.extend(sub_list2[::-1])
    return file_list


"""
The function loop_print(list)  takes in a list and out print all the elements as string in the list. It serves to print all the files 
from the file lists
"""


def loop_print(file_list: list) -> None:
    for file in file_list:
        print(str(file))

"""
This function is the first part of the project. First, it will loop through until the user enter an input 
that is in correct format which is a type string letter(D or R) followed by a space following bya valid path to a valid 
directory. It will print ERROR to indicate either the format is wrong, or the path the directory is invalid or the 
directory does not exist. If the format is correct and the directory is valid. The codes will store the files into a 
file list based on the type(D or R), and then print them out. 
"""


def get_files_from_directory():
    while True:
        try:
            medium_list = split()
            type = medium_list[0]
            p1 = Path(medium_list[1])
            list = []
            count = 0
            if medium_list[0] == "D" and Path(p1).exists():
                count += 1
                # if the type is D, we need to consider only the files in the directory
                for x in p1.iterdir():
                    if x.is_file():
                        list.append(x)
                        list.sort()
            elif medium_list[0] == "R" and Path(p1).exists():
                count += 1
                # if the type is R, we need to consider all the files in the directory and all the subdirectories and
                # the sub of the subs and so on
                list = print_dirt2(p1)
            if count > 0:
                break
            print("ERROR")
        except:
            print("ERROR")

    loop_print(list)
    return list

"""
This function is the second part of the main project. First it is given a file lists which contain all the 
selected files from the given directory and type in the first part of the project, then it reads input from the user 
until the user enter a correct input using readline() method which is explained in the method section above. Then the 
function will store all the interesting files into file list #2 based on the types in the input(A, N, E, T, <, >),
and then print the files out.
"""


def filter_files(file_list: list) -> list:
    list2 = []

    type, path = readline()
    if type == "A":
        # A means all the files in file list #1 are considered interesting
        list2 = file_list.copy()
    for file in file_list:
        if type == "N" and file.name == path:
            # if the type is N, all the files that have the same name as the user's input will be considered interesting
            list2.append(file)
        elif type == "E" and path == file.suffix[1:]:
            # if the type is E, all the files that have the same extension as the user's input will be considered
            # interesting
            list2.append(file)
        elif type == "T":
            # if the type is T, all the files that contains the same text as the user's input will be considered
            # but if the file is not text file or cannot be read, it won't be considered interesting, so I use try
            # to skip the non-text files
            try:
                lines = file.read_text()
                if path in lines:
                    list2.append(file)
            except:
                continue
        elif type == "<":
            # if the type is <, all the files that are small than the size of user's input will be considered
            if file.stat().st_size < path:
                list2.append(file)
        elif type == ">":
            # if the type is >, all the files that are bigger than the size of user's input will be considered
            if file.stat().st_size > path:
                list2.append(file)

    loop_print(list2)
    return list2


"""
This function is the last part, the action part of the project, first it will be given a file list that includes 
all the interesting files from the filter method, then it reads input from the users until they enter input in 
correct format, and then take actions to the files in the given file list based on the action type (F, D, T) 
"""

def take_action(file_list2: list) -> None:
    action_type = read_action_line()
    for files in file_list2:
        if action_type == "F":
            # if the type is F, we will print out the first line of all the files that are considered interesting
            # I use try to skip the files that can't be read
            try:
                f = open(files, "r")
                if files.stat().st_size == 0:
                    print("\r")
                else:
                    print(f.readline(), end="")
            except:
                print("NOT TEXT")
        if action_type == "D":
            # if the type is D, we create a duplicate file for all the files that are considered interesting
            # I use try to make different operation on text files and bytes files, but it seems like all of them
            # works as bytes files.
            new_file = files.parent / Path(files.name + ".dup")
            try:
                new_file.write_text(files.read_text())
            except:
                new_file.write_bytes(files.read_bytes())
        if action_type == "T":
            # if the type is T, we touch" the file, which means to modify its last modified timestamp to be the current
            # date/time
            files.touch(exist_ok=True)

"""
This function is the run/execution of the project. It conbines the three steps
of the project together step by step. 
"""
def run_function() -> None:
    file_list = get_files_from_directory()
    file_list2 = filter_files(file_list)
    if len(file_list2) > 0:
        take_action(file_list2)


run_function()
