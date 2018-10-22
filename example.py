from read_csv import read_csv
from simpletrend import *

pandas_tags = read_csv("pandas_tags.csv")


simpletrend = SimpleTrend()

for idx, row in pandas_tags.iterrows():
    simpletrend.index_tag(row)
    print(simpletrend.end_of_timestep_analysis())
    simpletrend.next_timestep()
    print('--------------------')
