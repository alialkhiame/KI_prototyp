from io import StringIO

import pandas as pd

import logging


def cleanData(data):
    # Lade Umsatzdaten aus einer CSV-Datei

    umsatz_data = data
    logging.info(data)
    # Entferne Zeilen mit fehlenden Werten
    umsatz_data = pd.read_csv(StringIO(umsatz_data))

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
