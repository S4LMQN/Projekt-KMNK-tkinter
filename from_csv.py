import csv
from os import path
import re

def unpack(file_path):
    if not path.exists(file_path):
        raise FileNotFoundError('Nieprawidłowa ściezka do pliku')
    
    if not re.match(r'.*\.csv$', file_path):
        raise FileExistsError("Plik nie jest typu .csv")
    
    dictionary = {}
    with open(file_path, 'r') as f:
        d = csv.DictReader(f)
        headers = d.fieldnames
        for row in d:
            for key, value in row.items():
                if key not in dictionary.keys():
                    dictionary[key] = [value]
                else:
                    dictionary[key].append(value)
    
    return dictionary

print(unpack("test.csv"))
