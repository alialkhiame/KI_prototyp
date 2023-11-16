import os

import os
import json
import csv

d = {"month":["month"],
     "Haupt Variablen" : ["Martial Kosten","Beschaffung Kosten, umwetterung"],
     "Wirtschaftliche Variablen" : ["Arbeitslosigkeitquote","Inflationsrate"],
     "Historsche Daten":["Gewinn", "kapital" , "Eigenkapital", "Fremd Kapital", "Umsatz"],
     "Wirtschaftliche Indikatoren": ["Bau Zinsen","GDP", "Arbeitslosigenqute", "inflationsrate"],
     "optionale Daten":["instal api", "x api", "facebook api"]
     }
#kosten the Year 2000 as a base line then the procent of the groth/schrenk of the price like : 2001 was 10% cheeper then 2000 and so on
#umwetterung 1 to ten: 1 snow and -10 or 40 degress and just too hot to work ---> 10 sunny and perfect to work
#arbeits. %
#inflation %
#Gewinn : baseline 2000 and then like 10 % more gewinn then 2001
#eigenkapital int
#fremdkapital int
#umsatz int
#inflation %
#Arbeitslosigenqute %
#"instal api", "x api", "facebook api" ints treated like a factors/ indecetors
#gdp int

import random

def generate_data(year):
    data = {"month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            "HauptVariablen": generate_haupt_variablen(year),
            "WirtschaftlicheVariablen": generate_wirtschaftliche_variablen(),
            "Historsche Daten": generate_historsche_daten(year),
            "WirtschaftlicheIndikatoren": generate_wirtschaftliche_indikatoren(),
            "optionaleDaten": generate_optionale_daten()
            }
    return data

def generate_haupt_variablen(year):
    martial_kosten = generate_baseline_value(2000)
    beschaffung_kosten_umwetterung = generate_baseline_value(2000)

    growth_percentage = random.uniform(0.9, 1.1)  # 10% variation

    martial_kosten *= growth_percentage
    beschaffung_kosten_umwetterung *= growth_percentage

    umwetterung = random.randint(1, 10)

    return [martial_kosten, beschaffung_kosten_umwetterung, umwetterung]

def generate_wirtschaftliche_variablen():
    arbeitslosigkeitquote = random.uniform(3, 15)
    inflationsrate = random.uniform(0, 5)

    return [arbeitslosigkeitquote, inflationsrate]

def generate_historsche_daten(year):
    baseline_values = {
        "Gewinn": 100000,
        "kapital": 500000,
        "Eigenkapital": 300000,
        "Fremd Kapital": 200000,
        "Umsatz": 1000000
    }

    growth_percentage = random.uniform(1.01, 1.2)  # 1-20% growth

    for key, value in baseline_values.items():
        baseline_values[key] *= growth_percentage

    return list(baseline_values.values())

def generate_wirtschaftliche_indikatoren():
    bau_zinsen = random.uniform(1, 5)
    gdp = random.uniform(100000, 500000)
    arbeitslosigenqute = random.uniform(3, 10)
    inflationsrate = random.uniform(0, 5)

    return [bau_zinsen, gdp, arbeitslosigenqute, inflationsrate]

def generate_optionale_daten():
    instal_api = random.randint(1, 100)
    x_api = random.randint(1, 100)
    facebook_api = random.randint(1, 100)

    return [instal_api, x_api, facebook_api]

def generate_baseline_value(base_year):
    return random.uniform(0.9, 1.1) * base_year

# Example usage:
year_to_generate = 2001
generated_data = generate_data(year_to_generate)
print(generated_data)

def save_data_to_csv(data, folder_path, base_filename):
    filename = f"{base_filename}_{len(os.listdir(folder_path)) + 1}.csv"
    filepath = os.path.join(folder_path, filename)

    with open(filepath, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data.items())

    return filename

def save_filename_to_text_file(filename, text_filepath):
    with open(text_filepath, 'a') as text_file:
        text_file.write(filename + '\n')

# Get the directory of the current script
current_directory = os.path.dirname(__file__)

# Specify the folder path where you want to save the files
output_folder = current_directory

# Generate data
year_to_generate = 2001
generated_data = generate_data(year_to_generate)

# Save data to CSV file and get the filename
file_name = save_data_to_csv(generated_data, output_folder, "generated_data")

# Save the filename to a text file
text_file_path = os.path.join(output_folder, "file_names.txt")
save_filename_to_text_file(file_name, text_file_path)
