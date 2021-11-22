import time
import datetime
import pandas as pd

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

# function to convert seconds to more readable format
def secs_to_pretty_time(seconds):
    """
    Convert time in secs to a detailed time string in days-hours-minutes-seconds.

    Returns:
        (str) detailed time string in days-hours-minutes-seconds where applicable.
    """
    if seconds >= 0:
        days = seconds // (24 * 3600)
        seconds = seconds % (24 * 3600)
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        seconds = seconds

        pretty_time = "%02d seconds" % (seconds)

        if days == 0 and hours == 0 and minutes > 0 :
            pretty_time = "%02d minutes %02d seconds" % (minutes, seconds)

        elif days == 0 and hours > 0 :
            pretty_time = "%02d hours %02d minutes %02d seconds" % (hours, minutes, seconds)

        elif days > 0 :
            pretty_time = "%02d days %02d hours %02d minutes %02d seconds" % (days, hours, minutes, seconds)
    else:
        raise TypeError("Wrong time format make sure that time is a positive integer or float!")
    
    return pretty_time


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    month = 'all'
    day = 'all'
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['chicago', 'new york city', 'washington']
    city = str(input('Please type a city name from (chicago/new york city/washington): ')).lower()
    while city not in cities:
        print('Wrong Entry!')
        city = str(input('Please type a city name from (chicago/new york city/washington): ')).lower()

    # get user input for filtering option
    options = ['both', 'month', 'day of week', 'no filter']
    option = str(input('Please choose filtering option from (month/day of week/both/no filter): ')).lower()
    while option not in options:
        print('Wrong Entry!')
        option = str(input('Please choose filtering option from (month/day of week/both/no filter): ')).lower()

    if option == 'month' or option == 'both':
        # get user input for month (all, january, february, ... , june)
        monthes = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        month = str(input('Please type a month name like (all, january, february, ... , june): ')).lower()
        while month not in monthes:
            print('Wrong Entry!')
            month = str(input('Please type a month name like (all, january, february, ... , june): ')).lower()

    if option == 'day of week' or option == 'both':
        # get user input for day of week (all, monday, tuesday, ... sunday)
        days_of_week = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = str(input('Please type a day name like (all, monday, tuesday, ... sunday): ')).lower()
        while day not in days_of_week:
            print('Wrong Entry!')
            day = str(input('Please type a day name like (all, monday, tuesday, ... sunday): ')).lower()

    print('-'*40)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Start Month: {}'.format(datetime.date(1900, common_month, 1).strftime('%B')))

    # display the most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Start Day of Week:', common_day_of_week)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]

    # Displaying hour in 12-hour clock time convention
    # Ugly for the Coder Pretty for the User
    common_start_hour = datetime.datetime.strptime(str(common_start_hour),'%H').strftime('%I:%M %p')
    print('Most Common Start Hour:', common_start_hour)


    # Too many decimals, limitation applied
    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Most Common Start Station:', common_start_station)


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Most Common End Station:', common_end_station)


    # display most frequent combination of start station and end station trip
    df['full_trip'] = df['Start Station'] + " ==> " + df['End Station']
    common_trip = df['full_trip'].mode()[0]
    print('Most Frequent Trip:', common_trip)

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time: {}'.format(secs_to_pretty_time(total_travel_time)))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean Travel Time: {}'.format(secs_to_pretty_time(mean_travel_time)))


    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df['User Type'].value_counts())
    print('Types of Users:')
    print('-'*15)
    for key, value in user_types.items():
        print('- There is {} {} User'.format(value, key))

    # Display counts of gender
    try:
        user_gender = dict(df['Gender'].value_counts())
        print('\nGender of Users:')
        print('-'*16)
        for key, value in user_gender.items():
            print('- There is {} {} User'.format(value, key))
    except:
        print("- Unfortunately Gender information is not available!")

    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode())
        print('\nEarliest Year of Birth:', earliest_birth_year)
        print('Most Recent Year of Birth:', recent_birth_year)
        print('Most Common Year of Birth:', common_birth_year)
    except:
        print("- Unfortunately Year of Birth information is not available!")

    print("\nThis took %s seconds." % round((time.time() - start_time), 3))
    print('-'*40)

def view_sample_raw_data(df):
    """
    View a Sample of raw data in sequence until user deny or no more data.
    """
    res = str(input('To view a sample of raw data enter "y" otherwise press any key: ')).lower()
    sample_size = 5
    if res == 'y':
        sample_size = str(input("Please enter the desired sample size (from 1 to 20): "))
        while sample_size not in [str(x) for x in range(1,21)]:
            print('Wrong Entry!')
            sample_size = str(input('Please enter the desired sample size (from 1 to 20): '))
        
        sample_size = int(sample_size)
        
        while res == 'y':
            if len(df.index) == 0:
                print('-'*40)
                print('You have reached the End of the Data !!')
                break
            elif len(df.index) < sample_size and len(df.index) > 0:
                print(df.sample(len(df.index)))
                print('-'*40)
                print('You have reached the End of the Data !!')
                break
            else:
                df_sample = df.sample(sample_size)
                print(df_sample)
                df = df.drop(df_sample.index) # remove previous rows
                print("{} rows remaining".format(len(df.index)))
                res = str(input('To view another sample enter "y" otherwise press any key: ')).lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        input("Press Enter to continue...")
        station_stats(df)
        input("Press Enter to continue...")
        trip_duration_stats(df)
        input("Press Enter to continue...")
        user_stats(df)
        view_sample_raw_data(df)

        restart = str(input('\nWould you like to restart? Enter yes or no.\n'))
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()