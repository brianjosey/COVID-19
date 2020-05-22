import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def prep_nyt_state_data():
	"""Downloads state-level COVID-19 data from the New York Times

	Args:
		none

	Returns:
		nyt_state_data (df): Contains all state-level data 
	"""


    NYT_STATE_URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    nyt_state_data = pd.read_csv(NYT_STATE_URL)
    return nyt_state_data


def prep_nyt_county_data():
	"""Downloads county-level COVID-19 data from the New York Times

	Args:
		none

	Returns:
		nyt_county_data (df): Contains all county-level data
	"""

	NYT_COUNTIES_URL = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
	nyt_counties_data = pd.read_csv(NYT_COUNTIES_URL)
	return nyt_counties_data


nyt_state_data = prep_nyt_state_data()
nyt_counties_data = prep_nyt_county_data()


def state_averages(state, window=7):
	"""Generates a dataframe for the state with daily and average cases/deaths.

	Function generates a dataframe using prep_nyt_state_data containing
	only the entries for the specified state. It then appends four new 
	columns containing the daily change in the number of cases and deaths
	and the average daily change for the number of days specified by the
	window argument.

	Args:
		state (str): Name of the state of interest
		window (int): How many days to average over
			(default is 7)

	Returns:
		state_data (df): Dataframe updated with daily/weekly changes
	"""
    state_data = nyt_state_data[nyt_state_data['state'] == state]
    state_data = state_data.reset_index(drop=True)

    # Append dataframe with daily change in cases/deaths
    state_data['daily_cases'] = state_data['cases'] - state_data['cases'].shift(1)
    state_data['daily_deaths'] = state_data['deaths'] - state_data['deaths'].shift(1)

    # Append dataframe with average daily change in cases/deaths
    state_data['average_cases'] = state_data.iloc[:,5].rolling(window).mean()
    state_data['average_deaths'] = state_data.iloc[:,6].rolling(window).mean()

    # Replace NaNs with 0
    state_data = state_data.fillna(0)
    return state_data


def plot_ave_case(state_df, STATE):
	"""Plots the daily and average number of cases in STATE

	Args:
		state_df (df): Dataframe for specified state.
		STATE (str): Name of the state

	Returns:
		plot: Plot of the daily change in the number of cases.
	"""
    days = np.array([i for i in range(len(state_df['date']))])

    fig, ax = plt.subplots(figsize = (16, 6))

    sns.lineplot(x=days, y=state_df['daily_cases'], sort=False, linewidth = 2, color = 'red')
    sns.lineplot(x=days, y=state_df['average_cases'], sort=False, linewidth = 4, color='black')

    plt.suptitle(f"COVID-19 Cases in {STATE}", fontsize=16, fontweight = 'bold')
    plt.ylabel('Number of Cases')
    plt.xlabel('Days Since First Case')

    ax.legend(['Deaths per Day', 'Weekly Average'])
    ax.fill_between(days, 0, state_df['daily_cases'], alpha=0.15, color='red')

    plt.show()


def plot_ave_deaths(state_df, STATE):
	"""Plots the daily and average number of deaths in STATE

	Args:
		state_df (df): Dataframe for specified state.
		STATE (str): Name of the state

	Returns:
		plot: Plot of the daily change in the number of deaths.
	"""

    days = np.array([i for i in range(len(state_df['date']))])

    fig, ax = plt.subplots(figsize = (16, 6))

    sns.lineplot(x=days, y=state_df['daily_deaths'], sort=False, linewidth = 2, color = 'red')
    sns.lineplot(x=days, y=state_df['average_deaths'], sort=False, linewidth = 4, color='black')

    plt.suptitle(f"COVID-19 Deaths in {STATE}", fontsize=16, fontweight = 'bold')
    plt.ylabel('Number of Deaths')
    plt.xlabel('Days Since First Case')

    ax.legend(['Deaths per Day', 'Weekly Average'])
    ax.fill_between(days, 0, state_df['daily_deaths'], alpha=0.15, color='red')

    plt.show()


def state_plot(state):
	"""Creates two plots, cases and deaths, for specified state.

	Args:
		state (str): Name of specified state.

	Returns:
		df (df): Dataframe for specified state.
		plots: Two plots, one of case the other of deaths.

	"""
    df = state_averages(state)
    plot_ave_case(df, state)
    plot_ave_deaths(df, state)