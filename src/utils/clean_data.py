import pandas as pd 
# Data cleaning: Types conversion and removing duplicates
def clean_data_set(data_frame:pd.DataFrame)->None:
    data_frame.set_index('Unnamed: 0', inplace=True)
    data_frame.drop_duplicates(subset=["locality", "price", "nb_bedrooms", "living_area"],inplace=True)


  # LOCALITY - removing missing values
    data_frame.dropna(subset=["locality"], inplace=True)

    # ZIP CODE - removing missing values + changing type
    data_frame.dropna(subset=['zip_code'], inplace=True)
    data_frame['zip_code'] = data_frame['zip_code'].astype(float).astype(int).astype(str)
    
    # PRICES - removing missing values
    data_frame.dropna(subset=["price"], inplace=True)
    # Removing values if we have some rows left with something else than the price in it (like life annuity)

    # SURFACE OF THE PLOT - remove rows with data that don't make sense
    data_frame.drop(data_frame[data_frame['surface_of_the_plot'] < 5].index, inplace = True)

    # NUMBER OF FACADES - remove rows when the facade is 1
    data_frame.drop(data_frame[(data_frame['nb_facades'] == 1)].index, inplace = True)

    # garden_surface  - replace 0 by None + remove rows with data that don't make sense
    data_frame['garden_surface'] = data_frame['garden_surface'].replace(0, None)
    data_frame.drop(data_frame[data_frame['garden_surface'] < 5].index, inplace = True)

    # terrace_surface - replace 0 by None + remove rows with data that don't make sense
    data_frame['terrace_surface'] = data_frame['terrace_surface'].replace(0, None)
    data_frame.drop(data_frame[data_frame['terrace_surface'] < 3].index, inplace = True)

    #Int conversion
    columns_to_convert_int = ['id','nb_bedrooms', 'garden_surface', 'terrace_surface', 'surface_of_the_plot', 'living_area','nb_facades']
    for col in columns_to_convert_int:
        data_frame[col] = pd.to_numeric(data_frame[col], errors='coerce')
        data_frame[col] = data_frame[col].astype('Int64')

    #String conversion
    print('id before conversion', data_frame['id'].dtype)
    columns_to_convert_str = ['id','property_type', 'locality', 'zip_code', 'state_of_building']
    for col in columns_to_convert_str:
        data_frame[col] = data_frame[col].astype(str)
    print('id after conversion', data_frame['id'].dtype)
    

    #float conversion
    data_frame['price'] = pd.to_numeric(data_frame['price'], errors='coerce').astype(float)
    # EXPORT NEW CSV 
    data_frame.to_csv('house_data_clean.csv', index=False)

