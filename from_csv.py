import csv
from os import path
import re

def read_csv(file_path):
    if not path.exists(file_path):
        raise FileNotFoundError('Nieprawidłowa ściezka do pliku')
    
    if not re.match(r'.*\.csv$', file_path):
        raise FileExistsError("Plik nie jest typu .csv")
    
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        d = csv.DictReader(f, delimiter=',')
        for row in d:
            for key, value in row.items():
                if key not in dictionary.keys():
                    dictionary[key] = [value]
                else:
                    dictionary[key].append(value)
    
    return dictionary
