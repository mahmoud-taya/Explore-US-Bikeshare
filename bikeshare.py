import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Choose city (chicago, new york city, washington): ')
    while city not in ['chicago', 'new york city', 'washington']:
        print('Please choose correct city')
        city = input('Choose City: ')

    # get user input for month (all, january, february, ... , june)
    month = input('Choose month (all, january, february, ... , june): ')

    while month not in ['january', 'february', 'mars', 'april', 'may', 'june', 'all']:
        print('Please choose correct month')
        month = input('Choose month (all, january, february, ... , june): ')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Choose day of week (all, monday, tuesday, ... sunday): ')
    while day not in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
        print('Please choose correct day')
        day = input('Choose day of week (all, monday, tuesday, ... sunday): ')
    print('*' * 50)
    return city, month, day


#############################################################
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    # convert time from string
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # get month and day name and hour from Start Time after convert
    df['month'] = df['Start Time'].dt.month
    df['day_name'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter month
    if month != 'all':
        months = ['january', 'february', 'mars', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by day
    if day != 'all':
        df = df[df['day_name'] == day.title()]

    return df


###############################################################

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('the most common Month: {}'.format(df['month'].mode()[0]))

    # display the most common day of week
    print('the most common day of week : {}'.format(df['day_name'].mode()[0]))

    # display the most common start hour
    print('the most common start hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


#########################################################################


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('the most common used start station: {}'.format(
        df['Start Station'].mode()[0]))

    # display most commonly used end station
    print('the most common used end station: {}'.format(
        df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    same_trip = df.groupby(['Start Station', 'End Station'])
    print(" common trip:\n {}".format(same_trip.size().sort_values().tail(1)))

    # second method to get common trip

    df['common_trip'] = df['Start Station'] + ' To ' + df['End Station']
    print('Most common Trip From: {}'.format(
        df['common_trip'].value_counts().head(1)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


#############################################################################

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('total travel time: {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('Average travel time: {} '.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


################################################################################

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    if city != 'washington':
        # Display counts of gender
        print(df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth

        print('most recent year: {}'.format(int(df['Birth Year'].max())))
        print('earliest year: {}'.format(int(df['Birth Year'].min())))
        print('most common year of birth: {}'.format(
            int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# =====================================================================

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print('►Bike share systems Statistic Data for {} ◄ '.format(city.capitalize()))
        print('=' * 50)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to continue? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
