import pandas as pd

def read_EV_table(filename):
    '''
    Reads file which contains data on Electric Vehicles and turns it into a DataFrame.
    '''
    file = pd.read_csv(filename, sep = ";")
    df = pd.DataFrame()
    df["vehicle_sort"] = file["Voertuigkenmerken"]
    df["period"] = file["Perioden"]
    df["vehicle1"] = file["Personenauto_2"]
    df["vehicle2"] = file["Camper_13"]

    return df

def get_data_info(df):
    '''
    Gives information on the data read from read_EV_table function.
    '''
    print(df.shape)
    print()
    print(df.info())
    print()
    print(df.describe())
    print()
    print(df.isna().sum())

def cleanup_data(df):
    '''
    Changes dtypes and adds NaN to missing values to df from read_EV_table function.
    Adds together columns vehicle1 and vehicle2 to correctly represent data.
    Years becomes separate columns.
    '''
    df = df.copy()

    years_str = df["period"].astype(str).str.replace("JJ00", "", regex = False).str.strip()
    df["period"] = pd.to_numeric(years_str, errors = "coerce")

    # missing values column [3]
    df["vehicle2"]= df["vehicle2"].fillna(0)

    # combine columns[2 and [3]
    df["total_amount_vehicles"] = df["vehicle1"] + df["vehicle2"]

    df = df.drop(columns = ["vehicle1", "vehicle2"])

    return df

def row_to_column(df):
    '''
    Turns values in row into columns by pivoting.
    '''
    df = df.copy()

    pivot = df.pivot(index = "vehicle_sort", columns = "period", values = "total_amount_vehicles")
    return pivot

data = read_EV_table('86361NED_TypedDataSet_20261122164439.csv')
clean = cleanup_data(data)
correct = row_to_column(clean)
