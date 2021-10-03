import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}

CITY_FILTER = ['chicago', 'new york', 'washington']

MONTH_FILTER = ['january', 'february', 'march', 'april', 'may', 'june']

DAY_FILTER = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

filters = {
    'city': None,
    'month': 'all',
    'day': 'all'
}

def _get_filter(category, options):
    """"
    Helper function to get filters.
        Args:
            (str) category - name of category to filter
            (list) options - haystack for the category

        Returns:
            (str) answer - the needle(s) found in haystack
    """
    while True:
        try:
            answer = input(
                "Please input your desired {}: ".format(category)).strip()

            # If 'all' is entered, then no filter is applied!
            if answer == 'all':
                #  city CANNOT accept 'all'... so, we handle that.
                if not category == 'city':
                    answer = 'all'
                    break
            if not answer:
                raise ValueError("{} CANNOT be blank.".format(category))
            if any(i.isdigit() for i in answer):
                raise ValueError("{} name MUST be alphabets only.".format(category))
            if answer.lower() in options:
                break
            else:
                raise ValueError("You haven't entered a valid {} name in our database!!!".format(category))

        except ValueError as e:
            print("oops!!!...", e)

    if answer:
        print("Good! You have selected {} ".format(answer.upper()))
        filters[category] = answer
    else:
        print("No filter applied for {}".format(category.upper()))

    return (answer.lower())

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("We have data for the following cities ==> Chicago || New York || Wahsington")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = _get_filter('city', CITY_FILTER)

    # get user input for month (all, january, february, ... , june)
    month = _get_filter('month', MONTH_FILTER)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = _get_filter('day', DAY_FILTER)

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
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df

def friendly_display():
    """
        Display a friendly logo and a reminder of our applied filter.
        The ANSII character (bike_logo.txt file) was generated at 'https://www.ascii-art-generator.org/'
    
    """
    # Print our awesome log
    with open('bike_logo.txt', 'r') as f:
        logo = f.read()
    print(logo)

    # Remind us of the city
    print("\nI am showing data for the city of  {}...".format(filters['city'].title()))

    # Remind us of the month(s) selected
    if filters['month'] == 'all':
        print("\nI am showing data for all available months...")
    else:
        print("\nI am showing data for the month of {}...".format(filters['month'].title()))

    # Remind us  of the day(s) selected
    if filters['day'] == 'all':
        print("\nI am showing data for all days of the week...")
    else:
        print("\nI am showing data for {}...".format(filters['day'].title()))

    print('-' * 40)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')

    start_time = time.time()

    # display the most common month
    common_month = df['Month'].mode()[0]
    print("\nThe most common month of travel is {}".format(common_month))

    # display the most common day of week
    common_weekday = df['Day of Week'].mode()[0]
    print("\nThe most common day of week of travel is {}".format(common_weekday))

    # display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("\nThe most common start hour for travel is {}".format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("\nThe total time travelled is {} seconds".format(total_travel_time))

    # display mean travel time
    men_travel_time = df['Trip Duration'].mean()
    print("\nThe mean travel time is {} seconds".format(men_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the stations."""

    print('\nCalculating station statistics...\n')
    start_time = time.time()

    # display popular start station
    start_station = df['Start Station'].mode()[0]
    print("Popular Start Station => {}".format(start_station))

    # display popular end station
    end_station = df['End Station'].mode()[0]
    print("\nPopular End Station => {}".format(end_station))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_dict = df['User Type'].value_counts().to_dict()
    print("\nThe USER TYPE are as follows:")
    for key, value in user_types_dict.items():
        print("{} => {}".format(key, value))

    # Display counts of gender
    try:
        gender_types_dict = df['Gender'].value_counts().to_dict()
        print("\nTher GENDER TYPE are as follows:")
        for key, value in gender_types_dict.items():
            print("{} => {}".format(key, value))
    except:
        print("\nData for gender is NOT available!")

        # Display earliest, most recent, and most common year of birth
    try:
        year = df['Birth Year']
        print("\nThe earliest birth year is {}. The most recent birth year is {}. The common year of birth is {}.".
              format(int(year.min()), int(year.max()), int(year.mode()[0])))
    except:
        print("\nData for birth year is NOT available!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_sample_data(df):
    browse_sample = input('\nWould you like to view sample data? Enter yes or no: \n')
    if browse_sample.lower() == 'yes':
        df_list = df.values.tolist()

        def chunker(lst):
            for i in range(0, len(lst), 5):
                yield df_list[i:i + 5]

        for chunk in chunker(df_list):
            print(list(chunk))
            is_continue = input("Enter Y to continue: ").strip()
            if is_continue.lower() != 'y':
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        friendly_display()

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_sample_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: \n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
