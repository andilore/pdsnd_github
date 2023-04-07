import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filters - filters to be applied to the df (e.g. 'month', 'day', 'month and day', or 'none' if no filters were applied)
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city data would you like to explore? Chicago, New York City, or Washington: ")
    
    while city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'washington':
        city = input("Error! That's not a valid input. Please enter one of: Chicago, New York City, or Washington: ")
        
    # parse the variable and set defaults
    city = city.lower().replace(" ","_")
    month = 'all'
    day = 'all'
    

    # get the user's filters of choice
    filters = input("Would you like to filter the data for month, day, both, or have no filter at all? Please enter 'month', 'day', 'both', or 'none': ")
    
    while (filters != 'month') and (filters != 'day') and (filters != 'both') and (filters != 'none'):
        filters = input("Error! That's not a valid input. Please enter one of: 'month', 'day', 'both', 'none': ")
    
    if (filters == 'month') or (filters == 'both'):
        # get user input for month (january, february, ... , june)
        month = input("Which month would you like to explore? January, February, ... June: ")
    
        while month.lower() != 'january' and month.lower() != 'february' and month.lower() != 'march' and month.lower() != 'april' and month.lower() != 'may' and month.lower() != 'june':
            month = input("Error! That's not a valid input. Please enter one of: January, February, March, April, May, or June:  ")
            
        # parse the variable
        month = month.lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
    if (filters == 'day') or (filters == 'both'): 
        # get user input for day of week (monday, tuesday, ... sunday)
        day = input("Which day of the week would you like to explore? Monday, Tuesday, etc.: ")
    
        while day.lower() != 'monday' and day.lower() != 'tuesday' and day.lower() != 'wednesday' and day.lower() != 'thursday' and day.lower() != 'friday' and day.lower() != 'saturday' and day.lower() != 'sunday':
            day = input("Error! That's not a valid input. Please enter one of: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or Saturday: ")
            
        # parse the variable
        day = day.title()

    if (filters == 'both'):
        filters = 'month and day'
    
    print('-'*40)
    return city, month, day, filters


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
    """

    # load data file into a dataframe
    filename = city + '.csv'
    df = pd.read_csv(filename)
    
    # create month and day_of_week columns - so can filter later
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month # extracts the month in a NUMERICAL value
    df['Day of week'] = df['Start Time'].dt.weekday_name # extracts the weekday NAME (not a number!)
    
    # filter by month and day of the week, if applicable
    if month != 'all':
        df = df[df['Month'] == month]
        
    if day != 'all':
        df = df[df['Day of week'] == day]
            

    return df


def time_stats(df, month, day, filters):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filters - filters that were applied to the df (e.g. 'month', 'day', 'month and day', or 'none' if no filters were applied)            
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        pop_month = df['Month'].mode()[0]
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        pop_month = months[pop_month -1]
        print("Most popular month: {}".format(pop_month))

    # TO DO: display the most common day of week
    if day == 'all':
        pop_day = df['Day of week'].mode()[0]
        print("Most popular day: {}".format(pop_day))

    # TO DO: display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Hour'].mode()[0]
    print("Most popular hour: {}".format(pop_hour))
    
    print("Filter used: {}".format(filters))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filters):
    """
    Displays statistics on the most popular stations and trip.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
        (str) filters - filters that were applied to the df (e.g. 'month', 'day', 'month and day', or 'none' if no filters were applied)

    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print("Most popular start station: {}".format(pop_start))

    # TO DO: display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print("Most popular end station: {}".format(pop_end))


    # TO DO: display most frequent combination of start station and end station trip
    highest_count_combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print("Most frequent combination of start station and end station: {}".format(highest_count_combo))
    
    print("Filter used: {}".format(filters))

                

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filters):
    """
    Displays statistics on the total and average trip duration.
    Args:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
        (str) filters - filters that were applied to the df (e.g. 'month', 'day', 'month and day', or 'none' if no filters were applied)

    """
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print("Total trip duration: {} seconds".format(total_duration))

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean()
    print("Mean trip duration: {} seconds".format(mean_duration))
    
    print("Filter used: {}".format(filters))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city, filters):
    """
    Displays statistics on bikeshare users.
    
    Args:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
        (str) city - name of the city to analyze
        (str) filters - filters that were applied to the df (e.g. 'month', 'day', 'month and day', or 'none' if no filters were applied)

    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    
    if city != 'washington':
        # TO DO: Display counts of gender
        gender = df['Gender'].value_counts()
        print(gender)

        # TO DO: Display earliest, most recent, & most common year of birth
        earliest_yob = int(df['Birth Year'].min(axis=0))
        print("Earliest year of birth: {}".format(earliest_yob))
          
        recent_yob = int(df['Birth Year'].max(axis=0))
        print("Most recent year of birth: {}".format(recent_yob))
          
        pop_yob = int(df['Birth Year'].mode()[0])
        print("Most common year of birth: {}".format(pop_yob))
    
    print("Filter used: {}".format(filters))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def view_indiv_data(df):
    """ 
    Displays individual trip data, 5 lines at a time.
        The user is prompted each time on whether they want to see another 5 lines of data
        
    Args:
        df - Pandas DataFrame containing city data filtered by month and day, if applicable
        
    """
    
    view_data = input('\nWould you like to view individual trip data? Type "yes" or "no": ')
    
    while (view_data != 'no') and (view_data != 'yes'):
        view_data = input('\nError! Please enter "yes" or "no": ')
        
    if view_data == 'yes':
        df = df.rename(columns={'Unnamed: 0': 'User Number'})
        num_rows, num_cols = df.shape
        num_rows_left = num_rows
        col_names = df.columns
        row_indices = df.index
        row_index_start = 0
        
    while (view_data == 'yes') and (num_rows_left > 0):
        if (num_rows_left >= 5):
            # display 5 rows
            for index in range(row_index_start, row_index_start+5):
                row_index = row_indices[index]                   
                for col_name in col_names:  
                    if (col_name != col_names[0]) and (col_name != col_names[(len(col_names)-1)]):
                        print("'" + str(col_name) + "': " + str(df.loc[row_index, col_name]))
                    elif (col_name == col_names[0]):
                        print("['" + str(col_name) + "': " + str(df.loc[row_index, col_name]))
                    elif (col_name == col_names[(len(col_names)-1)]):
                        print("'" + str(col_name) + "': " + str(df.loc[row_index, col_name]) + "]\n")                                                       
            row_index_start = row_index_start + 5
            num_rows_left = num_rows_left - 5
            
            if (num_rows_left != 0):
                view_data = input('\nWould you like to view more individual trip data? Type "yes" or "no": ')
            else:
                print("\nYou have reached the end of the dataset.")        

            
        else:
            # display remaining rows
            for index in range(row_index_start, row_index_start+num_rows_left):
                row_index = row_indices[index]
                for col_name in col_names:                           
                    if (col_name != col_names[0]) and (col_name != col_names[(len(col_names)-1)]):
                        print("'" + str(col_name) + "': " + str(df.loc[row_index, col_name]))
                    elif (col_name == col_names[0]):
                        print("['" + str(col_name) + "': " + str(df.loc[row_index, col_name]))
                    elif (col_name == col_names[(len(col_names)-1)]):
                        print("'" + str(col_name) + "': " + str(df.loc[row_index, col_name]) + "]\n")
            
            num_rows_left = 0
            print("\nYou have reached the end of the dataset.")            
            
            
def main():
    while True:
        city, month, day, filters = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day, filters)
        station_stats(df, filters)
        trip_duration_stats(df, filters)
        user_stats(df, city, filters)
        view_indiv_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
