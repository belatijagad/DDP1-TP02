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
def checker(key, row, row_num, pth, opt='cs'):
    keywords = key.split('*')
    if key.count('*') > 1:
        print('Argumen program tidak benar.')
        sys.exit()
    keywords = list(filter(None, keywords))
    if opt == 'cs':
        if len(keywords) == 1 and keywords[0] in row:
            print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
        elif len(keywords) == 2 and keywords[0] in row and keywords[1] in row and \
                early_checker(keywords[0], keywords[1], row):
            print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
    elif opt == '-i':
        if len(keywords) == 1 and keywords[0].casefold() in row.casefold():
            print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
        elif len(keywords) == 2 and keywords[0].casefold() in row.casefold() and \
                keywords[1].casefold() in row.casefold() and early_checker(keywords[0], keywords[1], row, opt):
            print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
    elif opt == '-w':
        if len(keywords) == 1:
            if (' ' + keywords[0] + ' ') in row:
                print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
            elif row.find(keywords[0]) == 0 and row[len(keywords[0])] == ' ':
                print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
            elif row.rfind(keywords[0]) == abs(len(row.strip()) - len(keywords[0])) and row.find(' ' + keywords[0]):
                print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')
        elif len(keywords) == 2 and early_checker(keywords[0], keywords[1], row) and keywords[0] in row and keywords[1] in row:
            if (' ' + keywords[0] in row or row.find(keywords[0]) == 0) and \
                    (keywords[1] + ' ' in row or row.find(keywords[1]) == len(row.strip())-len(keywords[1])):
                print(f'{pth:<40s} line {row_num:<3d} {row.strip():<40s}')

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
            (opt == '-i' and row.lower().find(first_split.lower()) < row.lower().rfind(second_split.lower())):
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
