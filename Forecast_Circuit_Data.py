import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Creating a list of forecasted dates from 1/1/2025-7/15/2025
date_list = pd.date_range(start='2025-01-01', end='2025-07-15', freq='D')

### Loop through all forecasted distribution circuits files
dist_df = pd.DataFrame()
for date in date_list:
    file_path = f'//sce.eix.com/workgroup/SPE_DSA/Charles/IgnitionGoalSettingInput/Dist_Forecasts 1-1-25 through 7-15-25/circuit_level_weather_fpi2_Distribution_HFA_{date.strftime("%Y%m%d")}.csv'
    # try reading file_path if possible and concat to result Dataframe
    try:
        df = pd.read_csv(file_path)
        df['Date'] = date.strftime('%Y-%m-%d')
        dist_df = pd.concat([dist_df, df], ignore_index=True)
    # if file does not exist, use the most recent date's file and get the new date from there
    except FileNotFoundError:
        print(f"File not found: {file_path}")
dist_df = dist_df[pd.to_datetime(dist_df['Datetime']).dt.year == 2025]

# create a list of Date ranges from 07-07 to today date
today = pd.to_datetime("today").strftime("%Y-%m-%d")
# use 8/26/2025 as today date since data goes up to this date so far
today = pd.to_datetime("2025-08-26")
date_ranges = pd.date_range(start='2025-07-16', end=today)
# create a list of valid dates
valid_dates = ['07-16-2025']
# create an empty dataframe for forecast data
forecast_file_group = pd.DataFrame()

# loop through date ranges
for date in date_ranges:
    try:
        print(date.strftime('%m-%d-%Y'))
        forecast_file = pd.read_csv(f"//sce.eix.com/workgroup/SPE_DSA/Charles/ADS_forecast/Dist Circuit FPI2 Forecast_{date.strftime('%m-%d-%Y')}.csv",)
        # add date to valid dates
        valid_dates.append(date.strftime('%m-%d-%Y'))
    except:
        print(f"File for {date.strftime('%m-%d-%Y')} not found, using previous valid date instead...")
        forecast_file = pd.read_csv(f"//sce.eix.com/workgroup/SPE_DSA/Charles/ADS_forecast/Dist Circuit FPI2 Forecast_{valid_dates[-1]}.csv",)
    # make sure date is in string format
    forecast_file['Date'] = pd.to_datetime(forecast_file['Datetime']).dt.strftime('%Y-%m-%d')
    # keep only current date
    forecast_file = forecast_file[forecast_file['Date'] == date.strftime('%Y-%m-%d')]
    # append to forecast_file_group
    forecast_file_group = pd.concat([forecast_file_group, forecast_file], ignore_index=True)
# sort by Circuit and Date
forecast_file_group = forecast_file_group.sort_values(by=['Circuit','Datetime']).reset_index(drop=True)

# create cols to keep for distribution circuits
cols_to_keep_dist = ['Datetime','Date','Circuit', 'FuelsIndex_max_FPI2', 'LFPwtdd_max_FPI2','Max_Wind','Max_Gust']
# concat dist_df with forecast_file_group
dist_df_with_forecast = pd.concat([dist_df[cols_to_keep_dist], forecast_file_group[cols_to_keep_dist]], ignore_index=True)
# save file to Distribution_Forecast_2025.csv
dist_df_with_forecast.to_csv('//sce.eix.com/workgroup/SPE_DSA/Charles/IgnitionGoalSettingMidput/Dist_Forecasts_2025.csv', index=False)