import pandas as pd
import numpy as np
import calendar
import time
from calendar import month_name

class DataGenerator:
    def __init__(self):
        # Setting the random seed for reproducibility
        np.random.seed(int(time.time()))

    def load_inflation_data(self, filename):
        # Load inflation data from the CSV file
        inflation_data = pd.read_csv(filename, delimiter=';', decimal=',')
        return inflation_data
    
    def load_zinsen_data(self, filename):
        # Load zinsen data from the CSV file
        zinsen_data = pd.read_csv(filename, delimiter=';', decimal=',')
        
        return zinsen_data
    
    def generate_umsatz_and_save_csv(self, num_years=10, inflation_file="inflation_values.csv", zinsen_file="zinsen_values.csv"):
        current_year = 2023
        years = list(range(current_year - num_years + 1, current_year + 1))

        # Table for monthly sales
        monthly_data = {
            "Jahr": [],
            "Monat": [],
            "Umsatz": [],
            "Unwetter": [],
            "Bodenrinnen": [],
            "Duschrinnen": [],
            "Berlin": [],
            "Hamburg": [],
            "Fulda": [],
            "Stuttgart": [],
            "Paris": []
        }

        # Table for aggregated yearly sales
        yearly_data = {
            "Jahr": [],
            "Umsatz": [],
            "Bodenrinnenanteil": [],
            "Duschrinnenanteil": [],
            "Baumarktanteil": [],
            "Objektgeschäft": [],
            "Private Bauherren": [],
            "Inflation in %": [],
            "Zinsen in %": []
    
        }

        # Table for daily sales
        daily_data = {
            "Jahr": [],
            "Monat": [],
            "Tag": [],
            "Umsatz": [],
            "Bodenrinnen": [],
            "Duschrinnen": [],
        }

        # Cumulative variables
        umsatz_steigungjahr = 1.05

        # Variables for generation
        Startumsatz = 65000
        Umsatz_steigerung_Sommer = 1.1
        random_negativ = -2500
        random_positiv = 2500
        unwetter_wahrscheinlichkeit = 0.15
        unwetter_wahrscheinlichkeitsminderung = 0.90

        # Load inflation data
        inflation_data = self.load_inflation_data(inflation_file)
        zinsen_data = self.load_zinsen_data(zinsen_file)

        for year in years:
            yearly_total_umsatz = 0  # For aggregated yearly sales

            # Read the corresponding inflation value for the year
            inflation_value = inflation_data.loc[inflation_data["Jahr"] == year, "Inflation"].values[0]

            # Read the corresponding zinsen value for the year
            zinsen_value = zinsen_data.loc[zinsen_data["Jahr"] == year, "Zinsen"].values[0]

            for month in range(1, 13):  # 12 months in a year
                monthly_data["Jahr"].append(year)
                monthly_data["Monat"].append(month_name[month])
                zinsenabzug = 1 - zinsen_value * 3 / 100

                # Higher sales from May to August
                if 5 <= month <= 8:
                    umsatz = (Startumsatz * umsatz_steigungjahr * Umsatz_steigerung_Sommer * inflation_value + np.random.randint(random_negativ, random_positiv)) * zinsenabzug 
                    monthly_data["Unwetter"].append("NEIN") 
                else:
                    # Reduce sales if the probability of bad weather is high
                    if (11 <= month or month <= 3) and np.random.rand() < unwetter_wahrscheinlichkeit:
                        umsatz = (Startumsatz * umsatz_steigungjahr * unwetter_wahrscheinlichkeitsminderung * inflation_value + np.random.randint(random_negativ, random_positiv)) * zinsenabzug
                        monthly_data["Unwetter"].append("JA") 
                    else:
                        umsatz = (Startumsatz * umsatz_steigungjahr * inflation_value + np.random.randint(random_negativ, random_positiv)) * zinsenabzug
                        monthly_data["Unwetter"].append("NEIN") 
                        

                umsatz_deutschland = umsatz * 0.8
                # Umsatzverteilung auf standorte
                umsatz_verteilung = [np.random.uniform(0.4,1) for _ in range(4)]
                umsatz_verteilung_summe = sum(umsatz_verteilung)

                # Skalierung, um sicherzustellen, dass die Summe der Umsätze dem umsatz_deutschland entspricht
                umsatz_verteilung = [umsatz * (umsatz_deutschland / umsatz_verteilung_summe) for umsatz in umsatz_verteilung]

                # Shuffle the list to distribute randomly
                np.random.shuffle(umsatz_verteilung)

                # Assign values to different locations
                hamburg_umsatz, berlin_umsatz, fulda_umsatz, stuttgart_umsatz = umsatz_verteilung

                # Split Umsatz into Bodenrinnen und Duschrinnen
                bodenrinnen_umsatz = 0.8 * umsatz
                duschrinnen_umsatz = 0.2 * umsatz
                paris_umsatz = 0.2 * umsatz

                # Round the sales values to 2 decimal places
                umsatz = round(umsatz, 2)
                bodenrinnen_umsatz = round(bodenrinnen_umsatz, 2)
                duschrinnen_umsatz = round(duschrinnen_umsatz, 2)
                berlin_umsatz = round(berlin_umsatz, 2)
                fulda_umsatz = round(fulda_umsatz, 2)
                hamburg_umsatz = round(hamburg_umsatz, 2)
                stuttgart_umsatz = round(stuttgart_umsatz, 2)
                paris_umsatz = round(paris_umsatz, 2)

                monthly_data["Umsatz"].append(umsatz)
                monthly_data["Bodenrinnen"].append(bodenrinnen_umsatz)
                monthly_data["Duschrinnen"].append(duschrinnen_umsatz)
                monthly_data["Berlin"].append(berlin_umsatz)
                monthly_data["Hamburg"].append(hamburg_umsatz)
                monthly_data["Fulda"].append(fulda_umsatz)
                monthly_data["Stuttgart"].append(stuttgart_umsatz)
                monthly_data["Paris"].append(paris_umsatz)

                # Daily sales distribution
                num_days_in_month = calendar.monthrange(year, month)[1]

                # Calculate the total monthly sales
                total_monthly_sales = umsatz

                # Initialize an array to store daily sales variations
                daily_sales_variations = np.random.uniform(0.5, 1, num_days_in_month)

                # Normalize the array so that the sum equals 1
                daily_sales_variations /= daily_sales_variations.sum()
            
                # Daily loop
                for day, daily_variation in zip(range(1, num_days_in_month + 1), daily_sales_variations):
                    daily_data["Jahr"].append(year)
                    daily_data["Monat"].append(month_name[month])
                    daily_data["Tag"].append(day)

                    # Adjust Umsatz for each day
                    daily_umsatz_variation = daily_variation * total_monthly_sales
                    daily_data["Umsatz"].append(round(daily_umsatz_variation, 2))
                    daily_data["Bodenrinnen"].append(round(0.2 * daily_umsatz_variation, 2))
                    daily_data["Duschrinnen"].append(round(0.8 * daily_umsatz_variation, 2))
                    
           
            yearly_total_umsatz += umsatz

            # Round all values to 2 decimal places
            yearly_total_umsatz = round(yearly_total_umsatz, 2)
            gesamt_bodenrinnen = 0.8 * yearly_total_umsatz
            gesamt_duschrinnen = 0.2 * yearly_total_umsatz
            baumarktanteil = 0.4 * yearly_total_umsatz
            objektgeschäft = 0.4 * yearly_total_umsatz
            private_bauherren = 0.2 * yearly_total_umsatz
            gesamt_bodenrinnen = round(gesamt_bodenrinnen, 2)
            gesamt_duschrinnen = round(gesamt_duschrinnen, 2)
            baumarktanteil = round(baumarktanteil, 2)
            objektgeschäft = round(objektgeschäft, 2)
            private_bauherren = round(private_bauherren, 2)

            inflation_value = inflation_value -1

            yearly_data["Jahr"].append(year)
            yearly_data["Umsatz"].append(yearly_total_umsatz)
            yearly_data["Bodenrinnenanteil"].append(gesamt_bodenrinnen)
            yearly_data["Duschrinnenanteil"].append(gesamt_duschrinnen)
            yearly_data["Baumarktanteil"].append(baumarktanteil)
            yearly_data["Objektgeschäft"].append(objektgeschäft)
            yearly_data["Private Bauherren"].append(private_bauherren)
            yearly_data["Inflation in %"].append(inflation_value * 100)
            yearly_data["Zinsen in %"].append(zinsen_value)

            # Cumulative application of sales growth
            umsatz_steigungjahr *= 1.05

        # Create DataFrames
        monthly_df = pd.DataFrame(monthly_data)
        yearly_df = pd.DataFrame(yearly_data)
        daily_df = pd.DataFrame(daily_data)

        # Save DataFrames to CSV files
        monthly_file_name = f"Monatlicher_Umsatz_{current_year - num_years + 1}_{current_year}.csv"
        yearly_file_name = f"Jährlicher_Gesamtumsatz_{current_year - num_years + 1}_{current_year}.csv"
        daily_file_name = f"Täglicher_Umsatz_{current_year - num_years + 1}_{current_year}.csv"

        monthly_df.to_csv(monthly_file_name, index=False, sep=";", decimal=",")
        yearly_df.to_csv(yearly_file_name, index=False, sep=";", decimal=",")
        daily_df.to_csv(daily_file_name, index=False, sep=";", decimal=",")

        # Return DataFrames
        return monthly_df, yearly_df, daily_df

# Example usage
data_gen = DataGenerator()
monthly_data, yearly_data, daily_data = data_gen.generate_umsatz_and_save_csv(num_years=10)