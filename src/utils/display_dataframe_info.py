from pandas import DataFrame

def display_dataframe_info(df: DataFrame)->None:
    is_getting_info = True

    while is_getting_info:
        """
        Displays detailed information about the given dataframe, allowing users to view general
        statistics or specific column information interactively.

        Args:
            df (DataFrame): The pandas dataframe to be analyzed. It contains the real estate data
                            scraped from the Immoweb property listings.

        Returns:
            None: The function outputs the information directly to the console, but does not return any values.
            
        Behavior:
            - Users can select to view general information about the dataframe, such as summary statistics
            and column data types.
            - Users can also choose to inspect specific columns for information such as data type, unique values,
            missing values, and range (for certain numerical columns).
            - The function will prompt the user for input and handle invalid column names gracefully.
        """
        info_option = input("Select an option of the info you want to know about: \n"
                        "1 - Dataframe general info \n"
                        "2 - Specific column info \n"
                        "Or press any other key to exit: ")
        match info_option:
            case('1'):
                print('Overview: ')
                print(df.describe())
                print('\n')
                print('D')
                print(df.info())
            case('2'):
                while True:
                    col = input('Specify a valid column name: ')
                    min_max_cols = ['price','nb_bedrooms', 'living_area','surface_of_the_plot','nb_facades', 'garden_surface', 'terrace_surface']
                    if col in df.columns:
                            print('\n')
                            print(f'{col.upper()} info: \n')
                            print(f"{col} data type: {df[col].dtype}")
                            print(f"Unique values: {df[col].value_counts().count()}")
                            print(f"Mode: {df[col].mode()}")
                            print(f"Missing values: {df[col].isna().sum()}")
                            if col in min_max_cols:
                                print(f"Lowest value: {df[col].min()}")
                                print(f"Highest value: {df[col].max()} \n")
                            break
                    else:
                        print(f"{col} : invalid column name")
            case _:
                print("Exiting information display.")
                break  