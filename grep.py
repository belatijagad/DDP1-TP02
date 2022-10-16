import sys
import os

mode, condition = 'cs', 'normal'

# Pengecekan argumen, jika tidak memenuhi ketentuan maka program akan berhenti.
if len(sys.argv) == 3:
    keyword, folder_name = sys.argv[1], sys.argv[2]
elif len(sys.argv) == 4:
    mode, keyword, folder_name = sys.argv[1], sys.argv[2], sys.argv[3]
    if (not mode == '-w') and (not mode == '-i'):
        print('Argumen program tidak benar.')
        sys.exit()
else:
    print('Argumen program tidak benar.')
    sys.exit()

# Pengecekan secara menyeluruh, memastikan output sesuai dengan option input
# Untuk wildcard -w akan menganggap valid spasi di antara kedua kata.
def checker(key, row, row_num, pth, opt='cs'):
    words = key.split('*')
    if key.count('*') > 1:
        print('Argumen program tidak benar.')
        sys.exit()
    words = list(filter(None, words))
    if opt == 'cs':
        if len(words) == 1 and words[0] in row:
            print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()))]:<40s}')
        elif len(words) == 2 and words[0] in row and words[1] in row and \
                early_checker(words[0], words[1], row):
            print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()))]:<40s}')
    elif opt == '-i':
        if len(words) == 1 and words[0].casefold() in row.casefold():
            print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()))]:<40s}')
        elif len(words) == 2 and words[0].casefold() in row.casefold() and \
                words[1].casefold() in row.casefold() and early_checker(words[0], words[1], row, opt):
            print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()))]:<40s}')
    elif opt == '-w':
        if len(words) == 1:
            if (' ' + words[0] + ' ') in row or row.find(words[0]) == 0 and row[len(words[0])] == ' ' or \
                    row.rfind(words[0]) == abs(len(row.strip()) - len(words[0])) and row.find(' ' + words[0]):
                print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()) )]:<40s}')
        elif len(words) == 2 and early_checker(words[0], words[1], row) and words[0] in row and words[1] in row:
            if (' ' + words[0] in row or row.find(words[0]) == 0) and \
                    (words[1] + ' ' in row or row.find(words[1]) == len(row.strip())-len(words[1])):
                print(f'{pth:<40s} line {row_num:<3d} {row.strip()[0:min(40, len(row.strip()) )]:<40s}')

# Pemeriksaan file satu persatu. Menjalankan function checker setiap iterasi
def scan_file(pth, key, opt='cs'):
    file = open(pth, 'r')
    row_num = 0
    for row in file:
        row_num += 1
        checker(key, row, row_num, pth, opt)
    file.close()

# Pengecekan apakah kata potongan (khusus wildcard) kedua mendahului kata pertama, jika iya, return False
def early_checker(first_split, second_split, row, opt='cs'):
    if (opt == 'cs' or opt == '-w') and row.find(first_split) < row.rfind(second_split) or \
            opt == '-i' and row.lower().find(first_split.lower()) < row.lower().rfind(second_split.lower()):
        if (opt == 'cs' or opt == '-w') and row.find(first_split) + len(first_split) - 1 < row.rfind(second_split) or \
                opt == '-i' and row.lower().find(first_split.lower()) + len(first_split) - 1 < row.lower().rfind(second_split.lower()):
            return True
    return False


# Program utama. Loop setiap file di directory dan membaca semua file yang berekstensi .txt
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
                    scan_file(path[0], keyword, mode)
        if checks == 0:
            print(f'Path {folder_name} tidak ditemukan.')
except FileNotFoundError:
    print(f'Path {folder_name} tidak ditemukan.')
