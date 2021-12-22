import time
import pandas as pd
import random

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

MONTHS_DATA = {'January': 'January',
               'February': 'February',
               'March': 'March',
               'April': 'April',
               'May': 'May',
               'June': 'June',
               'All': 'all'}

DAYS_DATA = {'Monday': 'Monday',
             'Tuesday': 'Tuesday',
             'Wednesday': 'Wednesday',
             'Thursday': 'Thursday',
             'Friday': 'Friday',
             'Saturday': 'Saturday',
             'Sunday': 'Sunday',
             'All': 'all'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    """Get city input"""
    while True:
        city_input = ''
        random_city = random.choice(list(CITY_DATA.keys()))
        try:
            city_input = input(
                " :) Input a city \n --> Choose between; {}. \n Press enter when blank to use \'{}\': ".format(
                    ', '.join(list(CITY_DATA.keys())), random_city)).lower().strip()

            if city_input == '':
                city_input = random_city

            city_check = CITY_DATA[city_input]
            city = city_input

            break
        except KeyError:
            print(" :( {} is not valid. Try, {}".format(city_input, random_city))
            print()

    """Get month input"""
    while True:
        month_input = ''
        try:
            month_input = input(" :) Input a month \n --> Choose between; {} \n : Press enter when black to show all months: ".format(', '.join(list(MONTHS_DATA.keys())))).title().strip()

            if month_input == '':
                month_input = 'All'

            month = MONTHS_DATA[month_input]

            break
        except KeyError:
            print(" :( {} is not valid. Try, {}".format(month_input, random.choice(list(MONTHS_DATA.keys()))))
            print()

    """Get day input"""
    while True:
        day_input = ''
        try:
            day_input = input(" :) Input a day \n --> Choose between; {}  \n : Press enter when black to show all days: ".format(', '.join(list(DAYS_DATA.keys())))).title().strip()

            if day_input == '':
                day_input = 'All'

            day = DAYS_DATA[day_input]

            break
        except KeyError:
            print(" :( {} is not valid. Try, {}".format(day_input, random.choice(list(DAYS_DATA.keys()))))
            print()

    print('-' * 40)

    return city, month, day


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

    """load data file into a dataframe"""
    df = pd.read_csv(CITY_DATA[city])

    """convert the Start Time column to datetime"""
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    """extract hour from the Start Time column to create an hour column"""
    df['hour'] = df['Start Time'].dt.hour

    """extract month of week from Start Time to create new columns"""
    df['month'] = df['Start Time'].dt.month

    """extract day of week from Start Time to create new columns"""
    """df['day_of_week'] = df['Start Time'].dt.weekday_name"""
    df['day_of_week'] = df['Start Time'].dt.day_name()

    """filter by month if applicable"""
    if month != 'all':
        """use the index of the months list to get the corresponding int"""
        month = list(MONTHS_DATA.values()).index(month) + 1

        """filter by month to create the new dataframe"""
        df = df[df['month'] == month]

    """filter by day of week if applicable"""
    if day != 'all':
        """filter by day of week to create the new dataframe"""
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    """Display the most common month"""
    print('The most common month: ', list(MONTHS_DATA.values())[int(df['month'].mode()[0]) - 1])

    """Display the most common day of week"""
    print('The most common day of week: ', df['day_of_week'].mode()[0])

    """Display the most common start hour"""
    print('The most common start hour: {} hrs'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    """Display most commonly used start station"""
    print('The most common used start station: ', df['Start Station'].mode()[0])

    """Display most commonly used end station"""
    print('The most common used End Station: ', df['End Station'].mode()[0])

    """Display most frequent combination of start station and end station trip"""
    print('The most frequent combination of start station and end station trip: ',
          (df['Start Station'] + ' to ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    """Display total travel time"""
    print('The total travel time:', df['Trip Duration'].sum())

    """Display mean travel time"""
    print('The mean travel time is: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    """Display counts of user types"""
    print('The trips counts by user types is, ')
    group_by_user_type = df['User Type'].value_counts()
    for index, trip in enumerate(group_by_user_type):
        print(" {}: {}".format(group_by_user_type.index[index], trip))

    print()

    """Display counts of gender"""
    if 'Gender' in df:
        print('The trip counts by gender,')
        group_by_gender = df['Gender'].value_counts()
        for index, trip in enumerate(group_by_gender):
            print(" {}: {}".format(group_by_gender.index[index], trip))
    else:
        print('Sorry, no gender stats available for this city.')

    """Display earliest, most recent, and most common year of birth"""
    if 'Birth Year' in df:
        print('The earliest year of birth: ', df['Birth Year'].min())
        print('The most recent year of birth: ', df['Birth Year'].max())
        print('The most common year of birth: ', df['Birth Year'].value_counts().idxmax())
    else:
        print('Sorry, no birth year stats available for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_rows(df):
    view_data = input("Would you like to view 5 rows of individual trip data?\n --> Enter 'yes' to view or anything else to skip: ").lower()
    if view_data != 'yes':
        return
    else:
        view_display = 'yes'
        start_loc = 0
        while view_display == 'yes':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_display = input("Do you wish to continue?\n--> Enter 'yes' to continue or anything else to exit: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_rows(df)

        restart = input("\nWould you like to restart?\n --> Enter 'yes' or anything else to exit.\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
