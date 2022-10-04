import sys
import os

mode, condition = 'cs', 'normal'

if len(sys.argv) == 3:
    keyword, folder_name = sys.argv[1], sys.argv[2]
elif len(sys.argv) == 4:
    mode, keyword, folder_name = sys.argv[1], sys.argv[2], sys.argv[3]
    if (not mode == '-w') ^ (mode == '-i'):
        print('Argumen program tidak benar.')
        sys.exit()
else:
    print('Argumen program tidak benar.')
    sys.exit()


def wholeword_checker(key, line, con='normal'):
    index_start = line.find(key)
    index_end = line.find(key) + len(key) - 1
    if con == 'start':
        if (index_start == 0 or key == '') or (line[index_start - 1] == ' '):
            return True
        else:
            return False
    if con == 'end':
        if (index_end == len(line) - 2 or key == '') or (line[index_end + 1] == ' '):
            return True
        else:
            return False
    if con == 'normal':
        if index_start == 0 and line[index_end + 1] == ' ':
            return True
        elif not index_start == 0 and not index_end == len(line) - 1:
            if line[index_start - 1] == ' ' and (line[index_end + 1] == ' ' or line[index_end + 1] == '\n'):
                return True
            else:
                return False
        elif index_end == index_start + len(key) - 1 and line[index_start - 1] == ' ':
            return True
        else:
            return False


def print_result(pth, row_num, line):
    print(f'{pth:<40s} line {row_num:<3d} {line.strip():<40s}')


def scan_file(pth, key, opt='cs'):
    file = open(pth, 'r')
    row_num = 0
    if key.count('*') == 0:
        for lines in file:
            row_num += 1
            if opt == 'cs' and key in lines:
                print_result(pth, row_num, lines)
            elif opt == '-w' and key in lines and wholeword_checker(key, lines, 'normal'):
                print_result(pth, row_num, lines)
            elif opt == '-i' and key.casefold() in lines.casefold():
                print_result(pth, row_num, lines)
    elif key.count('*') == 1:
        for lines in file:
            row_num += 1
            first_word, second_word = key.split('*')
            if opt == 'cs' and first_word in lines and second_word in lines and \
                    lines.find(first_word) < lines.find(second_word):
                print_result(pth, row_num, lines)
            elif opt == '-w' and wholeword_checker(first_word, lines, 'start')\
                    and wholeword_checker(second_word, lines, 'end'):
                print_result(pth, row_num, lines)
            elif opt == '-i' and first_word.casefold() in lines.casefold() and \
                    second_word.casefold() in lines.casefold():
                print_result(pth, row_num, lines)


try:
    if folder_name.endswith('.txt'):
        scan_file(folder_name, keyword, mode)
    else:
        checks = 0
        for dirpath, dirnames, filenames in os.walk(folder_name):
            checks += 1
            for files in filenames:
                if files.endswith('.txt'):
                    path = [os.path.join(dirpath, files)]
                    rel_path = path[0]
                    scan_file(rel_path, keyword, mode)
        if checks == 0:
            print(f'Path {folder_name} tidak ditemukan.')
except IOError:
    pass
