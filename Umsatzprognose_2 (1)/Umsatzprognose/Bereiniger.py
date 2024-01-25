import pandas as pd

# Lade Umsatzdaten aus einer CSV-Datei
csv_file_path = 'Monatlicher_Umsatz_2014_2023.csv'
umsatz_data = pd.read_csv(csv_file_path)

# Entferne Zeilen mit fehlenden Werten
umsatz_data = umsatz_data.dropna()

# Überprüfe und bereinige mögliche Ausreißer oder unplausible Werte
spalte_zum_pruefen = 'Umsatz'
prozentsatz = 90  # 

# Konvertiere die Spalte in numerische Werte oder entferne sie
umsatz_data[spalte_zum_pruefen] = pd.to_numeric(umsatz_data[spalte_zum_pruefen], errors='coerce')
umsatz_data = umsatz_data.dropna(subset=[spalte_zum_pruefen])

durchschnittswert = umsatz_data[spalte_zum_pruefen].mean()
untergrenze = durchschnittswert - (durchschnittswert * prozentsatz / 100)
obergrenze = durchschnittswert + (durchschnittswert * prozentsatz / 100)

umsatz_data = umsatz_data[
    (umsatz_data[spalte_zum_pruefen] >= untergrenze) & (umsatz_data[spalte_zum_pruefen] <= obergrenze)
]
