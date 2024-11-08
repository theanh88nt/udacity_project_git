import time
import pandas as pd
import numpy as np
from IPython.display import display

# Dictionary that maps city names to their respective data file names.
CITY_DATA = { 'chicago': 'chicago.csv',
              'newyork': 'new_york_city.csv',
              'washington': 'washington.csv' }

# Constants representing the column names in the data files.
START_TIME_COL = "Start Time"
END_TIME_COL = "End Time"
START_STATION_COL = "Start Station"
END_STATION_COL = "End Station"
USER_TYPE_COL = "User Type"
GENDER_COL = "Gender"
BIRTH_YEAR_COL = "Birth Year"
STATION_COL = "Start/End station"

# List of months, allowing for filtering by month.
MONTHS_OF_YEAR = ['all', 'jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
# List of days of the week, allowing for filtering by day.
DAYS_OF_WEEK = ['all','mon','tue','wed','thu','fri','sat','sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while(city not in CITY_DATA.keys()):
        city = input(f"Please enter a city from the following options  ({list(CITY_DATA.keys())}):").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = ""
    while(month not in MONTHS_OF_YEAR):
        month = input(f"Please enter a month from the following options ({MONTHS_OF_YEAR}): ").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while(day not in DAYS_OF_WEEK):
        day = input(f"Please enter a day of the week from the following options ({DAYS_OF_WEEK}): ").lower()

    print('-'*40)
    return city, month, day



def load_data(city, month, day):
    """Loads data for the specified city and filters by month and day if applicable."""
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert columns to datetime if they exist
    if START_TIME_COL in df.columns:
        df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
        df['month'] = df[START_TIME_COL].dt.month
        df['day_of_week'] = df[START_TIME_COL].dt.dayofweek
        df['hour'] = df[START_TIME_COL].dt.hour

    if END_TIME_COL in df.columns:
        df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL])

    # Calculate trip duration if start and end time columns exist
    if START_TIME_COL in df.columns and END_TIME_COL in df.columns:
        df['duration'] = df[END_TIME_COL] - df[START_TIME_COL]

    # Combine start and end stations for trip analysis
    if START_STATION_COL in df.columns and END_STATION_COL in df.columns:
        df[STATION_COL] = df[START_STATION_COL].astype(str) + " - " + df[END_STATION_COL]

    # Filter by month if applicable
    if month != 'all':
        month = MONTHS_OF_YEAR.index(month)
        df = df[df['month'] == month]

    # Filter by day of week if applicable
    if day != 'all':
        day = DAYS_OF_WEEK.index(day)
        df = df[df['day_of_week'] == day]

    return df
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Convert columns to datetime if they exist
    if START_TIME_COL in df.columns:
        df[START_TIME_COL] = pd.to_datetime(df[START_TIME_COL])
        df['month'] = df[START_TIME_COL].dt.month
        df['day_of_week'] = df[START_TIME_COL].dt.dayofweek
        df['hour'] = df[START_TIME_COL].dt.hour

    if END_TIME_COL in df.columns:
        df[END_TIME_COL] = pd.to_datetime(df[END_TIME_COL])

    # Calculate trip duration if start and end time columns exist
    if START_TIME_COL in df.columns and END_TIME_COL in df.columns:
        df['duration'] = df[END_TIME_COL] - df[START_TIME_COL]

    # Combine start and end stations for trip analysis
    if START_STATION_COL in df.columns and END_STATION_COL in df.columns:
        df[STATION_COL] = df[START_STATION_COL].astype(str) + " - " + df[END_STATION_COL]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating the Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Check if the START_TIME_COL column exists in the data
    if df is not None and START_TIME_COL not in df.columns:
        print(f"The [{START_TIME_COL}] column is not available for statistical analysis.")
        print("\nThis calculation took %s seconds." % (time.time() - start_time))
        print('-' * 40)
        return

    # TO DO: display the most common month
    if df is not None and 'month' in df.columns:
        mode_value = df['month'].mode()
        common_month = mode_value[0] if not mode_value.empty else "No data"
        month_name = MONTHS_OF_YEAR[common_month] if isinstance(common_month, int) else common_month
        print(f"Most common month: {month_name}")

    # TO DO: display the most common day of the week
    if df is not None and 'day_of_week' in df.columns:
        mode_value = df['day_of_week'].mode()
        common_day_of_week = mode_value[0] if not mode_value.empty else "No data"
        day_name = DAYS_OF_WEEK[common_day_of_week] if isinstance(common_day_of_week, int) else common_day_of_week
        print(f"Most common day of the week: {day_name}")

    # TO DO: display the most common start hour
    if df is not None and 'hour' in df.columns:
        mode_value = df['hour'].mode()
        common_hour = mode_value[0] if not mode_value.empty else "No data"
        print(f"Most common start hour: {common_hour} o'clock")

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # TO DO: display most commonly used start station
    # Ensure necessary columns exist for the analysis
    if START_STATION_COL in df.columns and END_STATION_COL in df.columns:
        # Most commonly used start station
        common_start_station = df[START_STATION_COL].mode()[0]
        print(f"Most commonly used start station: {common_start_station}")

        # TO DO: display most commonly used end station
        # Most commonly used end station
        common_end_station = df[END_STATION_COL].mode()[0]
        print(f"Most commonly used end station: {common_end_station}")
        
        # TO DO: display most frequent combination of start station and end station trip
        # Most frequent combination of start station and end station trip
        common_se_station = df[STATION_COL].mode()[0]
        print(f"Most frequent combination of start station and end station trip: {common_se_station}")
    else:
        print("The necessary columns for station statistics are not available in the data.")

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    # Ensure necessary columns exist for duration analysis
    if 'duration' in df.columns:
        # Total travel time
        total_time = df['duration'].sum()
        print(f"Total travel time: {total_time}")

        # TO DO: display mean travel time
        # Mean travel time
        mean_time = df['duration'].mean()
        print(f"Mean travel time: {mean_time}")
    else:
        print("The necessary columns for trip duration statistics are not available in the data.")

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if df is not None and 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Counts of user types:")
        print(user_types)
    else:
        print("The 'User Type' column is not available in the data.")

    # TO DO: Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("Counts of gender:")
        print(gender_counts)
    except KeyError:
        print("The 'Gender' column is not available in the data.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print(f"Earliest birth year: {earliest_birth_year}")
        print(f"Most recent birth year: {most_recent_birth_year}")
        print(f"Most common birth year: {most_common_birth_year}")
    except KeyError:
        print("The 'Birth Year' column is not available in the data.")

    print("\nThis calculation took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays raw data from the DataFrame."""
    row_index = 0
    while True:
        view_data = input('Would you like to see 5 rows of raw data? Enter yes or no: ').lower()
        if view_data == 'yes':
            print(df.iloc[row_index:row_index + 5])
            row_index += 5
            if row_index >= len(df):
                print("No more data to display.")
                break
        elif view_data == 'no':
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
