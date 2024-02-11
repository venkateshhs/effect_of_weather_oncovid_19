# Code to For Temperature-Covid data relationship
import os
import pandas as pd

import pandas.tseries.offsets


# function to load the Covid Excel(xlsx) files
def load_covid():
    path = "DataSource"
    files = os.listdir(path)
    print(files)
    df = pd.DataFrame()
    for f in files:
        Week_name = f[:8]
        filename = "DataSource/" + f
        data = pd.read_excel(filename, "statadata1", usecols="B:W", header=6, engine='openpyxl')
        data["Week"] = Week_name
        df = df.append(data)

    df.rename(columns={'MeldeLandkreis': 'Stadt', 'N1': 'PCR_pos_N', 'N2': 'PCR_pos_Hosp', 'N4': 'PCR_pos_Dec'},
              inplace=True)
    print(df)
    state_names = df.Stadt.unique()
    print(state_names)
    df = df.replace({'LK Ahrweiler' : 'Ahrweiler',
                        'LK Altenkirchen' : 'Altenkirchen',
                        'LK Alzey-Worms' : 'Alzey-Worms',
                        'LK Bad Dürkheim' : 'Bad Durkheim',
                        'LK Bad Kreuznach' : 'Bad Kreuznach',
                        'LK Bernkastel-Wittlich'  : 'Bernkastel-Wittlich',
                        'LK Birkenfeld'  : 'Birkenfeld',
                        'LK Bitburg-Prüm'  : 'Bitburg-Prum',
                        'LK Cochem-Zell' : 'Cochem-Zell',
                        'LK Donnersbergkreis' : 'Donnersbergkreis',
                        'LK Germersheim' : 'Germersheim',
                        'SK Frankenthal' : 'KS Frankenthal',
                        'SK Kaiserslautern' : 'KS Kaiserslautern',
                        'SK Koblenz' : 'KS Koblenz',
                        'SK Landau i.d.Pfalz' : 'KS Landau i.d.Pf.',
                        'SK Ludwigshafen' : 'KS Ludwigshafen',
                        'SK Mainz' : 'KS Mainz',
                        'SK Neustadt a.d.Weinstraße' : 'KS Neustadt a.d.W.',
                        'SK Pirmasens' : 'KS Pirmasens',
                        'SK Speyer' : 'KS Speyer',
                        'SK Trier' : 'KS Trier',
                        'SK Worms' : 'KS Worms',
                        'SK Zweibrücken' : 'KS Zweibrucken',
                        'LK Kaiserslautern' : 'Kaiserslautern',
                        'LK Kusel' : 'Kusel',
                        'LK Mainz-Bingen' : 'Mainz-Bingen',
                        'LK Mayen-Koblenz'  : 'Mayen-Koblenz',
                        'LK Neuwied' : 'Neuwied',
                        'LK Rhein-Hunsrück-Kreis' : 'Rhein-Hunsruck',
                        'LK Rhein-Lahn-Kreis' : 'Rhein-Lahn-Kreis',
                        'LK Rhein-Pfalz-Kreis' : 'Rhein-Pfalz-Kreis',
                        'LK Südliche Weinstraße' : 'Sudliche Weinstr.',
                        'LK Südwestpfalz' : 'Sudwestpfalz',
                        'LK Trier-Saarburg' : 'Trier-Saarburg',
                        'LK Vulkaneifel' : 'Vulkaneifel',
                        'LK Westerwaldkreis' : 'Westerwaldkreis'})
    return df


# function to load the Covid Excel(xlsx) files
def merge_csv(df):
    os.makedirs('CovidData', exist_ok=True)
    df.to_csv('CovidData/out.csv', index=False)
    csv_name = 'CovidData/out.csv'
    return csv_name

# function to load the Covid Excel(xlsx) files
def load_csv(csv):
    data = pd.read_csv(csv)
    return data


#function to load the weather file and aggregate it on weekly basis and save it as a new csv file
def weather_csv():
    filename = "CovidData/Temp_Aggregated_1Year.csv"
    data = pd.read_csv(filename)
    print(data)
    types = data.dtypes
    print(types)
    data['Current Date'] = pd.to_datetime(data['Current Date'])
    print(data)
    types = data.dtypes
    print(types)
    data['Week_Number'] = data['Current Date'].dt.isocalendar().week
    data['Year_Number'] = data['Current Date'].dt.year
    print(data)
    data['Week'] = data['Year_Number'].astype(str) + "KW" + data['Week_Number'].astype(str)
    print(data)
    types = data.dtypes
    print(types)
    aggrega = data.groupby(['Week', 'Stadt']).agg({'avg_temperature_per_day' : 'mean', 'max_temp_per_day' : 'mean', 'min_temp_per_day': 'mean', 'max - min temp': 'mean'}).reset_index()
    print(aggrega)
    aggrega.to_csv('CovidData/weather.csv', index=False)
    csv_name = 'CovidData/weather.csv'
    return csv_name


# the main function.
if __name__ == '__main__':
    #loading all csv covid files to one dataframe
    merged_df = load_covid()
    print(merged_df)

    #changing dataframe into to csv
    covid_csv_name = merge_csv(merged_df)

    #loading the weather file and aggregating into csv
    weather_csv_name = weather_csv()

    #Merging the covid and weather
    covid_df = load_csv(covid_csv_name)
    weather_df = load_csv(weather_csv_name)
    dataframe = pd.merge(covid_df, weather_df, on = ['Stadt', 'Week'], how='inner')
    dataframe.to_csv('CovidData/dataframe.csv', index=False)
    print(dataframe)

