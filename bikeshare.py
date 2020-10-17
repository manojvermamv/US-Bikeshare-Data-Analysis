# Python 3.8.5 Fully Supported
import time
import pandas as pd

City_Data = {'chicago': 'data/chicago.csv', 'new york': 'data/new_york_city.csv', 'washington': 'data/washington.csv'}
Months = ['january', 'february', 'march', 'april', 'may', 'june']
Days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

# print long string with repeating char, used to separate sections of output
line_length = 101
print_line = lambda string: print(f"<{string[0] * line_length}>")


def print_processing_time(start_time):
    time_str = "[... %s seconds]" % round((time.time() - start_time), 3)
    print(time_str.rjust(line_length))
    print_line('-')


def get_filter_city():
    """
    Asks user to specify a city.
    Returns:
        (str) city - name of the city to analyze
    """
    list_of_cities = []
    n_cities = 0

    for city in City_Data:
        list_of_cities.append(city)
        n_cities += 1
        print(f"\t{n_cities}. {city.title()}")

    while True:
        try:
            city_num = int(input(f"\n\tEnter the city number which you want to filter ( 1 - 3 ) : "))
        except:
            print("	----> Invalid Input !")
            continue

        if city_num in range(1, len(list_of_cities) + 1):
            break
        else:
            print("	----> Invalid Input !")
    city = list_of_cities[city_num - 1]
    return city


def get_filter_month():
    """
    Asks user to specify a month to filter on, or choose all.
    Returns:
        (str) month - name of the month to filter by, or "all" for no filter
    """
    list_of_months = []
    n_months = 0
    print()

    for month in Months:
        list_of_months.append(month)
        n_months += 1
        print(f"\t{n_months}. {month.title()}")

    while True:
        month_num = input(f"\n\tEnter the month number which you want to filter ( 1 - 6 ) or 'a' for all months : ")
        if month_num == 'a':
            month = 'all'
            break
        elif month_num in str(list(range(1, 7))):
            month = Months[int(month_num) - 1]
            break
        else:
            print("	----> Invalid Input !")
    return month


def get_filter_day():
    """
    Asks user to specify a day to filter on, or choose all.
    Returns:
        (str) day - day of the week to filter by, or "all" for no filter
    """
    list_of_days = []
    n_days = 0
    print()

    for day in Days:
        list_of_days.append(day)
        n_days += 1
        print(f"\t{n_days}. {day.title()}")

    while True:
        day_num = input(f"\n\tEnter the day number which you want to filter ( 1 - 7 ) or 'a' for all days : ")
        if day_num == 'a':
            day = 'all'
            break
        elif day_num in {'1', '2', '3', '4', '5', '6', '7'}:
            day = Days[int(day_num) - 1]
            break
        else:
            print("	----> Invalid Input !")
    return day


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print_line('-')
    print("\n\tHello! Let's explore some US bikeshare data!\n")

    # get user input for city (chicago, new york, washington)
    city = get_filter_city()
    # get user input for month (all, january, february, ... , june)
    month = get_filter_month()
    # get user input for day of week (all, monday, tuesday, ... , sunday)
    day = get_filter_day()

    return city, month, day


def filter_summary(city, month, day, init_total_rides, df):
    """
    Displays selected city, filters chosen, and simple stats on dataset.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (int) init_total_rides - total number of rides in selected city before filter
        (dataframe) df - filtered dataset
    """
    start_time = time.time()

    filtered_rides = len(df)
    start_station_no = len(df['Start Station'].unique())
    end_station_no = len(df['End Station'].unique())

    print(f"\tGathering statistics for {city}...")
    print("\t   Filtered ( Month & Day )  :     ", month, '&', day)
    print("\t   Total rides in dataset    :     ", init_total_rides)
    print("\t   Rides in filtered dataset :     ", filtered_rides)
    print("\t   Number of start stations  :     ", start_station_no)
    print("\t   Number of end stations    :     ", end_station_no)

    print_processing_time(start_time)


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
    start_time = time.time()

    # load data into a DataFrame called 'df'
    df = pd.read_csv(City_Data[city])

    # convert the Time columns to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'], errors='coerce')
    df['End Time'] = pd.to_datetime(df['End Time'], errors='coerce')

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    init_total_rides = len(df)

    # Drop 'Unnamed' column if applicable in 'df'

    # filter by month if applicable
    if month == 'all':
        # use the index of the MONTHS list to get the corresponding int
        month_i = Months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df.month == month_i]
        month = month.title()

    # filter by day of week if applicable
    if day == 'all':
        # use the index of the WEEKDAYS list to get the corresponding int
        day_i = Days.index(day) + 1

        # filter by day of week to create the new dataframe
        df = df[df.day_of_week == day_i]
        day = day.title()

    print_processing_time(start_time)
    filter_summary(city.title(), month, day, init_total_rides, df)
    return df


def hour_12_str(hour):
    """
    Converts an int hour time to string format with PM or AM.
    Args:
        (int) hour - int representing an hour
    Returns:
        (str) str_hour - string with time in 12 hour format
    """
    if hour == 0:
        str_hour = '12 AM'
    elif hour == 12:
        str_hour = '12 PM'
    else:
        str_hour = f"{ str(hour)+' AM' if hour < 12 else str(hour-12)+' PM' }"
    return str_hour


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    start_time = time.time()
    print('\tMost Frequent Times of Travel...')

    # display the most common month; convert to string
    common_month = Months[df['month'].mode()[0] - 1].title()
    print("\t   Month        :    ", common_month)

    # display the most common day of week
    common_day = Days[df['day_of_week'].mode()[0]].title()
    print("\t   Day          :    ", common_day)

    # display the most common start hour; convert to 12-hour string
    common_hour = hour_12_str(df['hour'].mode()[0]).title()
    print("\t   Start hour   :    ", common_hour)

    print_processing_time(start_time)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    start_time = time.time()
    print('\tMost Popular Stations and Trip...')
    filtered_rides = len(df)

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    start_station_trip = df['Start Station'].value_counts()[start_station]
    print("\t   Start station     :   ", start_station)
    print(f"{' ' * 35}{start_station_trip}/{filtered_rides}")

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    end_station_trip = df['End Station'].value_counts()[end_station]
    print("\t   End station       :   ", end_station)
    print(f"{' ' * 35}{end_station_trip}/{filtered_rides}")

    # display most frequent combination of start station and end station trip
    # group the results by start station and end station
    start_end_combination = df.groupby(['Start Station', 'End Station'])
    most_freq_trip_count = start_end_combination['Trip Duration'].count().max()
    most_freq_trip = start_end_combination['Trip Duration'].count().idxmax()
    print(f"\t   Frequent trip     :    {most_freq_trip[0]}, {most_freq_trip[1]}")
    print(f"{' ' * 35}{most_freq_trip_count} trips")

    print_processing_time(start_time)


def seconds_to_HMS_str(total_seconds):
    """
    Converts number of seconds to human readable string format.
    Args:
        (int) total_seconds - number of seconds to convert
    Returns:
        (str) day_hour_str - number of weeks, days, hours, minutes, and seconds
    """

    minutes, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)

    day_hour_str = ''
    if weeks > 0:
        day_hour_str += f"{weeks} weeks, "
    if days > 0:
        day_hour_str += f"{days} days, "
    if hours > 0:
        day_hour_str += f"{hours} hours, "
    if minutes > 0:
        day_hour_str += f"{minutes} minutes, "
    if total_seconds > 59:
        day_hour_str += f"{seconds} seconds"
    return day_hour_str


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    start_time = time.time()
    print("\tTrip Duration...")

    # display total travel time; cast to int, we don't need fractions of seconds!
    total_travel_time = int(df['Trip Duration'].sum())
    print(f"\t   Total travel time   :  {seconds_to_HMS_str(total_travel_time)}")

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print(f"\t   Mean travel time    :  {seconds_to_HMS_str(mean_travel_time)}")

    print_processing_time(start_time)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    start_time = time.time()
    print("\tUser Stats...")
    user_types = df['User Type'].value_counts()
    for idx in range(len(user_types)):
        value = user_types[idx]
        user_type = user_types.index[idx]
        print(f"\t   {user_type }        :       {value}")

    # 'Gender' and 'Birth Year' is only available for Chicago and New York City
    # Check for these columns before attempting to access them
    if 'Gender' in df.columns:
        # Display counts of gender
        genders = df['Gender'].value_counts()
        for idx in range(len(genders)):
            value = genders[idx]
            gender = genders.index[idx]
            print(f"\t   {gender}            :       {value}")

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        print("\n\t   Year of Birth...")
        print("\t      Earliest        :   ", int(df['Birth Year'].min()))
        print("\t      Most Recent     :   ", int(df['Birth Year'].max()))
        print("\t      Most Common     :   ", int(df['Birth Year'].mode()))

    print_processing_time(start_time)


def display_raw_data(df):
    """
    Asks if the user would like to see some lines of data from the filtered dataset.
    Displays 5 (show_rows) lines, then asks if they would like to see 5 more.
    Continues asking until they say stop.
    """
    show_rows = 5
    rows_start = 0
    rows_end = show_rows - 1
    print("\tWould you like to see some raw data from the current dataset?")
    while True:
        raw_input = input("\t   ('y' or 'n')   :  ")
        if raw_input.lower() == 'y':
            # display show_rows number of lines, but display to user as starting from row as 1
            # e.g. if rows_start = 0 and rows_end = 4, display to user as "rows 1 to 5"
            print(f"\n\tDisplaying rows {rows_start + 1} to {rows_end + 1} ...")

            print("\n", df.iloc[rows_start : rows_end + 1])
            rows_start += show_rows
            rows_end += show_rows

            print_line('-')
            print(f"\n\t   Would you like to see the next {show_rows} rows?")
            continue
        else:
            break


if __name__ == '__main__':
    while True:
        city, month, day = get_filters()
        dataframe = load_data(city, month, day)

        time_stats(dataframe)
        station_stats(dataframe)
        trip_duration_stats(dataframe)
        user_stats(dataframe)
        display_raw_data(dataframe)

        restart = input("\tWould you like to restart? (y or n): ")
        if restart.lower() != 'y':
            break
