import pandas as pd
import numpy as np 

# importing data from csv file  2019_Q2, 2019_Q2,2019_Q3 
data_2=pd.read_csv("Divvy_Trips_2019_Q4.csv",header=0  )
data_3=pd.read_csv("Divvy_Trips_2019_Q3.csv",header=0  )
data_4=pd.read_csv("Divvy_Trips_2019_Q2.csv",header=0  )

# replace blank into NA
data_2.fillna('NA', inplace=True)
data_3.fillna('NA', inplace=True)
data_4.fillna('NA', inplace=True)

# 2019_Q4 have same column as 2019_Q2 & 2019_Q3 but name is different so  changed 2019_Q4 columns names
# rename column name in data_4 
data_4.columns= ['trip_id', 'start_time', 'end_time', 'bikeid', 'tripduration', 'from_station_id', 'from_station_name', 'to_station_id', 'to_station_name', 'usertype', 'gender', 'birthyear']

# mergering data into single dataframe 
pd_list=[data_4,data_3,data_2]
f_df_1=pd.concat(pd_list, ignore_index=True)

# bikeid column not in 2020_Q1 so we need  to remove it and 
# tripduration column datatype have int64 and float mix so need remove it and we can get these column useing python 
#droping column i.e., bikeid, tripduration
f_df_1.drop(f_df_1.iloc[:, 3:5], inplace=True, axis=1)
print(f_df_1.info(), "\n ")

# same as bikeid.  gender , birthyear we need to remove it 
#droping column i.e., gender, birthyear
f_df_1.drop(f_df_1.iloc[:, 9:11], inplace=True, axis=1)


# gettting time difference which we droped due to mix datype

# couverting two columnes into datetime 
f_df_1['start_time']=pd.to_datetime(f_df_1['start_time'])
f_df_1['end_time']=pd.to_datetime(f_df_1['end_time'])

# getting difference 
f_df_1['time_diff']=f_df_1['end_time'] - f_df_1['start_time']

#converting time delta to seconds
f_df_1['time_diff']= f_df_1['time_diff'] / np.timedelta64(1, 's')

# shift column 'Name' to first position
first_column = f_df_1.pop('time_diff')

# insert column using insert(position,column_name,
# first_column) function
f_df_1.insert(3, 'time_diff', first_column)

# converting column trid id into string so that it matches wtih f_df_2 dtype
f_df_1['trip_id']= f_df_1['trip_id'].astype('str')

#saving data of 2019 in csv
#f_df_1.to_csv("2019_Q_2_to_4.csv")


###########################################################################################


#importing 2020_Q1 data 
f_df_2=pd.read_csv("Divvy_Trips_2020_Q1.csv", header=0)

#droping column start_lat, start_lng, end_la, end_lng they are only in 2020_Q1 files
f_df_2.drop(f_df_2.iloc[:, 1:2], inplace=True, axis=1)
f_df_2.drop(f_df_2.iloc[:, 7:11], inplace=True, axis=1)

# 2020_Q1 files has the different name but same datype 
# rename column in dataframe
f_df_2.rename(columns= {'ride_id': 'trip_id', 'started_at': 'start_time', 'ended_at': 'end_time', 'start_station_name':'from_station_name', 'start_station_id' :'from_station_id', 'end_station_name':'to_station_name', 'end_station_id':'to_station_id', 'member_casual':'usertype'}, inplace =True)

#for finding time diff
# converting two columnes into datetime 
f_df_2['start_time']=pd.to_datetime(f_df_2['start_time'])
f_df_2['end_time']=pd.to_datetime(f_df_2['end_time'])

# getting difference 
f_df_2['time_diff']=f_df_2['end_time'] - f_df_2['start_time']

#converting time delta to seconds
f_df_2['time_diff']= f_df_2['time_diff'] / np.timedelta64(1, 's')

# shift column 'Name' to first position
first_column = f_df_2.pop('time_diff')

# insert column using insert(position,column_name,
# first_column) function
f_df_2.insert(3, 'time_diff', first_column)


final_data_list=[f_df_1, f_df_2]
final_file=pd.concat(final_data_list, ignore_index=True)

final_file.to_csv("year_data.csv")
