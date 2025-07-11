import csv
from os import path

def read_csv(file_path):

    if not file_path.endswith(".csv"):
        raise FileExistsError("Plik nie jest typu .csv")
        
    if not path.exists(file_path):
        raise FileNotFoundError('Nieprawidłowa ściezka do pliku')
    
    dictionary = {}
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        d = csv.DictReader(f, delimiter=';')
        for row in d:
            for key, value in row.items():
                if type(value) == str:
                    if key not in dictionary.keys():
                        dictionary[key] = [value]
                    else:
                        dictionary[key].append(value)
                else: 
                    raise TypeError("Błędna wartość lub nierówna długość kolumn")
    
    return dictionary

def clean(raw_vals):
    cleaned = []
    for item in raw_vals:
        item = item.replace("\xa0", "")
        num = float(item.replace(" ", ""))
        cleaned.append(num)
    return cleaned
