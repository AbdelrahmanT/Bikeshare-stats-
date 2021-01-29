import time
import pandas as pd


# commonly used global data
city_data = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months=['january','february','march','april','may','june']
days=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def input_checker(valid_data,input_msg, err_msg='\ninvalid input, check your input and try again...\n' ):
    """
    Checks if input value is valid
    Args:
        (list,dict or similar) valid_data: a data structure with all valid input
        (str) input_msg: first message that appears to user requesting their input
        (str) err_msg: error message that appears to user when invalid input is entered
    Returns:
        (str) datum - data inputted by the user
        
    """
    datum=''
    while(True):
        datum =  input(input_msg).lower()
        if datum in valid_data:
            return datum
        print(err_msg)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str or None) month - name of the month to filter by, or None to apply no month filter
        (str or None) day - name of the day of week to filter by, or None to apply no day filter
    """
    month, day= None, None
    
    print('Hello! Let\'s explore some US bikeshare data!\n' )
    
    city = input_checker(city_data,
                         'Which city would you like to see data from?\nchicago, new york or washington?\n',
                       'You have entered an invalid city please make sure you have entered the name correctly!')
                       
    #filter input
    fltr = input_checker(['month','day','both','none'],
                        'Would you like to filter the data by month, day, both or none?\n')
   
    #month input
    if fltr == 'month' or fltr== 'both':
        month = input_checker(months,
                      'which month would you like to filter by?\njanuary ,february ,march ,april ,may or june? (type out full month name).\n')    
   
    #day input
    if fltr == 'day' or fltr== 'both':
        day=input_checker(days,
                      'which day would you like to filter by? type out full day name (e.g. sunday).\n')
        
    return city, month, day
    

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str or None) month - name of the month to filter by, or None to apply no month filter
        (str or None) day - name of the day of week to filter by, or None to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #load data file into data frame and create month and week columns
    df = pd.read_csv(city_data[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    if month!= None:
        df = df[df['month'] == month.title()]
    
    if day != None:
        df = df[df['day_of_week'] == day.title()]
        
    print('-'*40)    
        
    return df



def time_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    
    Args:
        (df) - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month 
    print('Most popular month of travel: ',df['month'].mode()[0])

    # display the most common day of week 
    print('Most popular day of travel: ',df['day_of_week'].mode()[0])

    # display the most common start hour
    print('Most popular hour of travel: ',df['Start Time'].dt.hour.mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    
    Args:
        (df) - Pandas DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most popular start station: ',df['Start Station'].mode()[0])

    # display most commonly used end station
    print('Most popular end station: ',df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print('Most popular combination of stations: ',(df['Start Station'] + ' , ' + df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.
    
    Args:
        (df) - Pandas DataFrame containing city data filtered by month and day
    
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total time travelled:',df['Trip Duration'].sum(),' seconds.')

    # display mean travel time
    print('Average time travelled:',df['Trip Duration'].mean(),' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """
    Displays statistics on bikeshare users.
    
    Args:
        (df) - Pandas DataFrame containing city data filtered by month and day
    
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df['User Type'].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print(df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest year of birth: ',df['Birth Year'].min(),
              '\nmost recent year of birth: ',df['Birth Year'].max(),
              '\nmost common year of birth: ',df['Birth Year'].mode())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_individual_data(df):
    """
    Parameters
    ----------
    df : Pandas DataFrame
        containing city data filtered by month and day.
        
    Returns
    -------
    None.

    """
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    is_all_data_shown = False
    while (view_data != 'no' and not is_all_data_shown):
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input('Do you wish to continue?: ').lower()
      is_all_data_shown = (start_loc + 5) > int(df.shape[0])
    if is_all_data_shown:
        print('We have no more data left, you have seen it all!')
        
        
def main():
        while True:
            df = load_data(*get_filters())  
    
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_individual_data(df)
            
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no':
                break
        
if __name__ == "__main__":
	main()

    


   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   
    
   