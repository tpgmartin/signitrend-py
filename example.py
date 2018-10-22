from read_csv import read_csv
from simpletrend import *

pandas_tags = read_csv("pandas_tags.csv")


simpletrend = SimpleTrend()

for idx, row in pandas_tags.iterrows():
    print(idx, row["tag_name"], row["creation_year_month"], row["tag_count"], row["all_tags_count"])
    print(simpletrend.index_tag(row))
    print('-------------------------')
