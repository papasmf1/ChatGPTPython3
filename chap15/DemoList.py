import os

# Get the list of all files and directories in the current working directory
dir_list = os.listdir('.')

print("Files and directories in '", os.getcwd(), "' :")

# prints all files
for item in dir_list:
    print(item)
