import pandas as pd 

houses = pd.read_csv("house_data.csv", encoding='utf-8')

# Having a general look at the dataframe
def checking_general_info():    
    print("General info about the dataset :")
    # Having a look at the dataframe
    print(houses.head(20))
    # Getting the columns name
    print(houses.columns)
    # Checking general info
    print(houses.info())
    # Checking the type of each column to see if some need to be changed 
    print(houses.dtypes)
    # Checking how many missing values we have for each column
    print(houses.isnull().sum()) 

# Having a look at one column
def checking_column_info():
    for column in houses.columns:
        print(f"info about {column}")
        # Checking the different values and how many there are
        print(houses[column].value_counts())
        print()


# Changing the type of a column values - TO BE USED IF ONE TYPE IS NOT CORRECT IN THE DATASET
def float_to_int(column_name):
    houses[column_name].apply(lambda x: int(x) if x is pd.notna else x)
    # Checking if the type has been changed to int
    # print(houses["column_name"].dtypes)
def float_to_str(column_name):
    houses[column_name] = houses[column_name].astype(float).astype(str)

# Having a look at the biggest and smallest values to see if there are some strange values
def check_values(column_name):
    print(f"Min & max for {column_name}")
    print(houses[column_name].min())
    print(houses[column_name].max())
    print(f"Looking at the highest and smallest values for {column_name}")
    houses_highest = houses[[column_name, "property_type"]].sort_values(by=[column_name], ascending=False)
    print("Higher numbers")
    print(houses_highest.head(20))
    houses_smallest = houses[[column_name, "property_type"]].sort_values(by=[column_name], ascending=True)
    print("Smaller numbers")
    print(houses_smallest.head(20))
    #to get the links of the 1st ones once it is sorted
    # observation = houses[0:10]
    # print(observation["link"])


# DUPLICATES
houses.set_index('Unnamed: 0', inplace=True)
print(houses.shape)
houses.drop_duplicates(subset=["locality", "price", "nb_bedrooms", "living_area"],inplace=True)
print(houses.shape)

checking_general_info()

# CHECKING ALL COLUMNS to see if there are strange values, ...
checking_column_info()
# PROPERTY
print(houses["property_type"].unique())
# PRICES
check_values("price")
# NUMBER OF BEDROOMS
check_values("nb_bedrooms")
# LIVING AREA
check_values("living_area")
# SURFACE OF THE PLOT
check_values("surface_of_the_plot")
# NUMBER OF FACADES
check_values("nb_facades")
# GARDEN SURFACE
check_values("Garden surface")
# TERRACE
check_values("Terrace surface")

print(houses.dtypes)

# Changing the types for some columns
float_to_str("zip_code")
# float_to_int("nb_bedrooms")
houses["nb_bedrooms"] = houses["nb_bedrooms"].apply(lambda x: x.astype(int) if type(x) != None else x)
float_to_int("living_area")
float_to_int("surface_of_the_plot")
float_to_int("nb_facades")
float_to_int("Garden surface")
float_to_int("Terrace surface")

print(houses.dtypes)

# LOCALITY - removing missing values
houses.dropna(subset=["locality"], inplace=True)

# ZIP CODE - removing missing values + changing type
houses.dropna(subset=["zip_code"], inplace=True)

# PRICES - removing missing values
houses.dropna(subset=["price"], inplace=True)
# Removing values if we have some rows left with something else than the price in it (like life annuity)
# houses = houses[houses["price"].str.contains("month") == False]

# SURFACE OF THE PLOT - remove rows with data that don't make sense
houses.drop(houses[houses['surface_of_the_plot'] < 5].index, inplace = True)

# NUMBER OF FACADES - remove rows when the facade is 1 and it's not an apartment or flat studio
houses.drop(houses[((houses['property_type'] != "Apartment") | (houses['property_type'] != "Flat_Studio")) & (houses['nb_facades'] == 1)].index, inplace = True)


# Garden surface  - remove rows with data that don't make sense
houses['Garden surface'] = houses['Garden surface'].replace(0, None)
houses.drop(houses[houses['Garden surface'] < 5].index, inplace = True)

# TERRACE SURFACE - remove rows with data that don't make sense
houses['Terrace surface'] = houses['Terrace surface'].replace(0, None)
houses.drop(houses[houses['Terrace surface'] < 3].index, inplace = True)

# EXPORT NEW CSV 
houses.to_csv('houses-clean.csv', index=False)

