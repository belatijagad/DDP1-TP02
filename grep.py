import sys
import os

folder_name, keyword, mode = 'mydir', 'mat pag', True

if len(sys.argv) == 3:
    keyword = sys.argv[1]
    folder_name = sys.argv[2]
elif len(sys.argv) == 4:
    mode = sys.argv[1]
    keyword = sys.argv[2]
    folder_name = sys.argv[3]


def is_whole_word(line, word):
    first_index = line.find(word)
    last_index = first_index + len(word)
    if word in line:
        if line[first_index - 1] == ' ' and line[last_index] == ' ':
            return True
        else:
            return False
    else:
        return False


def scan_file(paths, word, opt='cs'):
    file = open(paths, 'r')
    if opt == '-w':
        row = 0
        for line in file:
            if is_whole_word(line, word):
                row += 1
                splitted_words = word.split('*')
                if len(splitted_words) == 1:
                    if splitted_words[0] in line:
                        print(f'{paths:<40s} line {row:<3d} {line.strip():<40s}')
                elif len(splitted_words) == 2:
                    if splitted_words[0] in line and splitted_words[1] in line:
                        print(f'{paths:<40s} line {row:<3d} {line.strip():<40s}')
                else:
                    print('what')

    elif opt == '-i':
        row = 0
        for line in file:
            row += 1
            splitted_words = word.split('*')
            if len(splitted_words) == 1:
                if splitted_words[0] in line:
                    print(f'{paths:<40s} line {row:<3d} {line.strip():<40s}')
            elif len(splitted_words) == 2:
                if splitted_words[0] in line and splitted_words[1] in line:
                    print(f'{paths:<40s} line {row:<3d} {line.strip():<40s}')
    else:
        print('Input tidak valid.')
    file.close()


for dirpath, dirnames, filenames in os.walk(folder_name):
    for files in filenames:
        if files.endswith('.txt'):
            path = [os.path.join(dirpath, files)]
            rel_path = path[0]
            scan_file(rel_path, keyword, mode)
