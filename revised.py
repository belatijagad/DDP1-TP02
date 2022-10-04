import sys
import os

mode = 'cs'

if len(sys.argv) == 3:
    keyword = sys.argv[1]
    folder_name = sys.argv[2]
elif len(sys.argv) == 4:
    mode = sys.argv[1]
    keyword = sys.argv[2]
    folder_name = sys.argv[3]


def is_whole_word(key, line):
    first_index = line.find(key)
    last_index = first_index + len(key) - 1
    if (line[first_index - 1] == ' ' and line[last_index + 1] == ' ')\
            or (first_index == 0 and line[last_index + 1] == ' ')\
            or (line[first_index - 1] == ' ' and last_index == len(line) - 1):
        return True
    else:
        return False


def is_wild_card(key):
    if key.count('*') == 1:
        return True
    else:
        return False


def print_result(pth, row_num, line):
    print(f'{pth:<40s} line {row_num:<3d} {line.strip():<40s}')


def scan_file(pth, key, opt='cs'):
    file = open(pth, 'r')
    if opt == 'cs':
        row = 0
        for line in file:
            row += 1
            if key in line:
                print_result(pth, row, line)
    elif opt == '-i':
        row = 0
        for line in file:
            row += 1
            if key.casefold() in line.casefold():
                print_result(pth, row, line)
    elif opt == '-w':
        row = 0
        for line in file:
            row += 1
            if key in line and is_whole_word(key, line):
                print_result(pth, row, line)


try:
    if folder_name.endswith('.txt'):
        scan_file(folder_name, keyword, mode)
    else:
        for dirpath, dirnames, filenames in os.walk(folder_name):
            for files in filenames:
                if files.endswith('.txt'):
                    path = [os.path.join(dirpath, files)]
                    rel_path = path[0]
                    scan_file(rel_path, keyword, mode)
except IndexError:
    pass
