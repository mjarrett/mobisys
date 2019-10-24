import pandas as pd
import numpy as np

def prep_sys_df(f): 
    
    if f[-4:] == '.csv':
        df = pd.read_csv(f,low_memory=False)
    elif f[-5:] == '.xlsx':
        df = pd.read_excel(f)
        
    #df = df[df['Membership Type']!='VIP']

    df['Duration (min.)'] = df['Duration (sec.)'].map(lambda x: x/60)

    stations_exclude = ['station for tests','WareHouse Workshop','Balancer Bike Check In','Temporary Station - Marketing Events']
    df = df[~df['Departure station'].isin(stations_exclude)]
    df = df[~df['Return station'].isin(stations_exclude)]

    # Drop duplicate trips:
    # This removes cases where multiple bikes take the same trip on the same account
    # Also will remove cases where someone takes the same trip within an hour.
    df = df.drop_duplicates(subset=['Departure','Return','Account','Departure station','Return station'])

    # Drop trips shorter than 60 seconds
    df = df[df['Duration (sec.)']>60]

    # Get average speed
    df['average speed (km/h)'] = (df['Covered distance (m)']/1000) / ((df['Duration (sec.)']-df['Stopover duration (sec.)'])/3600)
    
    df = df.dropna()
    
    df['Departure'] = pd.to_datetime(df['Departure'])
    df['Return'] = pd.to_datetime(df['Return'])
    
    
    
    return df


def get_mem_types(df):
    
    idx24 = list(df['Membership Type']=='24 Hour')
    idx365 = list(df['Membership Type'].str.contains('365.+Standard'))
    idx365p = list(df['Membership Type'].str.contains('365.+Plus'))
    idx365all = list(df['Membership Type'].str.contains('365'))
    idx90 = list(df['Membership Type'].str.contains('90'))
    
    return idx24,idx365,idx365p,idx365all,idx90


def add_station_coords(df,sdf,drop=True):
    
    """
    WARNING: This drops records if the listed Departer/Return station name
             isn't in the stations_df.json file"
             To change this behaviour use drop=False. In this case, unknown stations
             are given (0,0) coords
    """

    if drop:
        how='inner'
    else:
        how='left'
    
    # Convert geometry to lat/long coords and drop geometry columns
    sdf = sdf.to_crs(epsg=4326)
    #sdf['coordinates'] = sdf['geometry'].map(lambda x: (x.y,x.x))
    sdf['lat'] = sdf['geometry'].map(lambda x: x.y)
    sdf['long'] = sdf['geometry'].map(lambda x: x.x)
    
    del sdf['geometry']
    
    
    sdf = sdf[sdf['lat'] >1 ]   # drop stations that don't have a sensible latitude

    df = pd.merge(df,sdf[['name','neighbourhood','lat','long']],how=how,left_on='Departure station',right_on='name',
                  suffixes=('_x',' departure'))

    df = pd.merge(df,sdf[['name','neighbourhood','lat','long']],how=how,left_on='Return station',right_on='name',
                  suffixes=(' departure',' return'))

    

    df = df.rename(columns={'neighbourhood return':'Return neighbourhood',
                    'neighbourhood departure':'Departure neighbourhood',
                    'lat return':'Return lat',
                    'lat departure':'Departure lat',
                    'long return':'Return long',
                    'long departure':'Departure long'})
    del df['name departure']
    del df['name return']

#     df['Departure coords'] = df['Departure coords'].apply(lambda x: (0, 0) if x is np.nan else x)
#     df['Return coords'] = df['Return coords'].apply(lambda x: (0, 0) if x is np.nan else x)
    df['Departure lat'] = df['Departure lat'].fillna(0)
    df['Return lat'] = df['Return lat'].fillna(0)
    df['Departure long'] = df['Departure long'].fillna(0)
    df['Return long'] = df['Return long'].fillna(0)    

#     df['stations coords'] = df[['Departure coords','Return coords']].values.tolist()
#     df['stations'] = df[['Departure station','Return station']].values.tolist()
    
    
#     if bidirectional:
#         df['stations coords'] = df['stations coords'].map(lambda x: tuple(sorted(x)))
#     else:
#         df['stations coords'] = df['stations coords'].map(lambda x: tuple(x))
#     df['stations'] = df['stations'].map(lambda x: tuple(sorted(x)))
    


    return df



def make_con_df(df):
    
    
    #condf = df.groupby(['stations coords','stations']).size()
    condf = df.groupby(['Departure station','Return station','Departure lat','Return lat','Departure long','Return long']).size()
    condf = condf.reset_index()
    condf.columns = ['Departure station','Return station','Departure lat','Return lat','Departure long','Return long','trips']
    
#     condf['start coords'] = condf['stations coords'].map(lambda x: x[0])
#     condf['stop coords'] = condf['stations coords'].map(lambda x: x[1])
#     condf['start station'] = condf['stations'].map(lambda x: x[0])
#     condf['stop station'] = condf['stations'].map(lambda x: x[1])
    return condf

def make_thdf(df):
    thdf = df.pivot_table(index='Departure', 
                     columns='Departure station', 
                     values='Account',
                     fill_value=0, 
                     aggfunc='count')
    return thdf

def make_rhdf(df):
    thdf = df.pivot_table(index='Return', 
                     columns='Return station', 
                     values='Account',
                     fill_value=0, 
                     aggfunc='count')
    return thdf

def make_ahdf(df):
    thdf = make_thdf(df)
    rhdf = make_rhdf(df)
    
    return rhdf.reindex(thdf.index).fillna(0) + thdf


