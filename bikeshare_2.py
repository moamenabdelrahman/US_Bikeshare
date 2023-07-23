import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

#stores the city inserted by user to use later in checking condition
City = ''

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington).
    city = ''
    while city not in CITY_DATA:
        city = input("Choose the city to analyze among (chicago, new york city or washington): ").strip().lower()

    # get user input for month (all, january, february, ... , june)
    month = ''
    months_filter = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months_filter:
        month = input("Enter name of the month to filter by, or \"all\" to apply no month filter: ").strip().lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ''
    days_filter = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'All']
    while day not in days_filter:
        day = input("Enter name of the day of week to filter by, or \"all\" to apply no day filter: ").strip().title()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    #stores the city inserted by user to use later in checking condition
    global City
    City = city
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load city.csv file
    df = pd.read_csv(CITY_DATA[city])
    #converting time columns into datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors = 'coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], errors = 'coerce')
    #extract month and day from 'Start Time' to new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()

    #do the filtering
    if month != 'all':
        df = df[df['Month'] == (months.index(month) + 1)]
    if day != 'All':
        df = df[df['Day'] == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #extract hour from 'Start time' to new column
    df ['Start Hour'] = df['Start Time'].dt.hour
    # display the most common month
    print("The most common month is {}\n".format(months[(df['Month'].mode()[0]) - 1].title()))

    # display the most common day of week
    print("The most common day of week is {}\n".format(df['Day'].mode()[0]))

    # display the most common start hour in am/pm system
    comm_hour = df['Start Hour'].mode()[0]
    if comm_hour == 0:
        print("The most common start hour is the midnight hour\n")
    elif comm_hour < 12:
        print("The most common start hour is {} am\n".format(comm_hour))
    elif comm_hour == 12:
        print("The most common start hour is the noon hour\n")
    else:
        print("The most common start hour is {} pm\n".format(comm_hour - 12))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    #combining start station and end station into new column ('trip')
    df['Trip'] = 'From ' + df['Start Station'] + ' To ' + df['End Station']

    # display most commonly used start station
    print("The most commonly used start station is {}\n".format(df['Start Station'].mode()[0]))

    # display most commonly used end station
    print("The most commonly used end station is {}\n".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    print("The most frequent trip is: {}\n".format(df['Trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    #dictionary of amount of seconds in a year, a month, and so on
    time_eq = {'year': 31104000, 'month': 2592000, 'day': 86400, 'hour': 3600, 'minute': 60, 'second': 1}
    #function takes quantity of seconds and returns a list of an equivalent form of seconds quantity as ()years, ()months, ..., ()seconds
    def convert(time):
        units_list = []
        x = 0
        for i in time_eq.values():
            units_list.append(time // i)
            time -= (units_list[x] * i)
            x += 1
        return units_list

    # display total travel time
    total = df['Trip Duration'].sum()
    list = convert(total)
    print("The total travel time is {} seconds which are equivalent to {} years, {} months, {} days, {} hours, {} minutes and {} seconds\n".format(total, list[0], list[1], list[2], list[3], list[4], list[5]))

    # display mean travel time
    print("The mean travel time is {} seconds\n".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    for type, count in dict(df['User Type'].value_counts()).items():
        print('There is/are {} {}(s)'.format(count, type))
    print()

    #washington city has no columns of gender and birth, so checking that to handle errors
    if City == 'washington':
        print("This city has no data about Gender and Birth year")
    else:
        # Display counts of gender
        for gender, num in dict(df['Gender'].value_counts()).items():
            print('There is/are {} {}(s)'.format(num, gender))

        # Display earliest, most recent, and most common year of birth
        list = []
        birth_year = pd.DataFrame(df, columns = ['Birth Year'])
        birth_year.dropna(axis = 0, inplace = True)
        list.append(int(birth_year.min()[0]))
        list.append(int(birth_year.max()[0]))
        list.append(int(birth_year.mode().values[0, 0]))
        print("\nThe earliest, most recent, and most common year of birth are: {}, {}, and {}".format(list[0], list[1], list[2]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        """
        Raw data is displayed upon request by the user in the following manner:

        1.Script prompts the user if they want to see 5 lines of raw data,
        2.Display that data if the answer is 'yes',
        3.Continue iterating these prompts and displaying the next 5 lines of raw data at each iteration,
        4.Stop the program when the user says 'no' or there is no more raw data to display.
        """
        raw_data = ''
        x, y = 0, 5

        while raw_data != 'no':
            raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').strip().lower()
            if raw_data != 'no':
                print(df[:][x:y])
                x += 5
                y += 5
            if y >= len(df):
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.strip().lower() == 'no':
            break

if __name__ == "__main__":
	main()
