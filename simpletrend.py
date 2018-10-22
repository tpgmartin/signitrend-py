import pandas as pd

class SimpleTrend():

    def __init__(self, bias: float = 1E-5, significance_threshold: float = 6.0, window_size: int = 12):
        self.bias = bias
        self.buckets = []
        self.frequency_map = dict()
        self.significance_threshold = significance_threshold
        self.stats_map = dict()
        self.cumulative_tag_count = 0
        self.time_step = 1
        self.trending_tags = []
        self.window_size = window_size

    # df columns: tag_name, creation_year_month, tag_count, all_tags_count
    # creation_year_month should be in chronological order
    # This has to be applied each timestep
    def index_tag(self, tag_row):

        tag_name = tag_row["tag_name"]
        frequency = self.frequency_map.get(tag_name, 0)
        self.frequency_map[tag_name] = frequency + tag_row["tag_count"]
        self.cumulative_tag_count += tag_row["all_tags_count"]
        bucket = self._get_or_set_tag_bucket(tag_name)

        if tag_name not in self.stats_map:
            mean, std = bucket["ewma"], bucket["ewmvar"]
            self.stats_map[tag_name] = (mean, std)

        # Can ignore below as this is to do with early alerting only
        # if tag_name in self.stats_map:
        #     mean, std = self.stats_map[tag_name]
        # else:
        #     mean, std = bucket["ewma"], bucket["ewmvar"]
        
        # relative_frequency = self._get_relative_frequency(self.frequency_map[tag_name])
        # significance = self._get_significance(mean, std, relative_frequency)

        # if self._is_significant(significance):
        #     return (tag_name, significance)

    # timestep is implicitly assumed to be calendar month
    def end_of_timestep_analysis(self):

        for tag_name in self.frequency_map:
            # mean, std = self.stats_map[tag_name]
            # This is temporary
            bucket = self._get_or_set_tag_bucket(tag_name)
            mean, std = bucket["ewma"], bucket["ewmvar"]
            relative_frequency = self._get_relative_frequency(self.frequency_map[tag_name])

            significance = self._get_significance(mean, std, relative_frequency)
            print(significance)
            if self._is_significant(significance):
                self.trending_tags.append((tag_name, significance))
        
        return self.trending_tags
    
    def next_timestep(self):
        # don't need update_table as considering unique tags individually only
        for tag_name in self.frequency_map:
            relative_frequency = self._get_relative_frequency(self.frequency_map[tag_name])
            bucket = [bucket for bucket in self.buckets if bucket["tag_name"] == tag_name][0]
            self._update_bucket(relative_frequency, bucket)
        
        self.time_step += 1
        self.trending_tags = []

    def _update_bucket(self, relative_frequency: float, bucket: dict):
        data = bucket["data"]
        data.loc[len(data)] = relative_frequency

        # rolling window for data
        data.drop(0, inplace=True)
        data.reset_index(inplace=True)
        del data["index"]

        window = data.ewm(adjust=True, span=self.window_size)
        bucket["data"] = data
        bucket["ewma"] = window.mean().iloc[self.window_size - 1][0]
        bucket["ewmvar"] = window.var().iloc[self.window_size - 1][0]

    def _get_or_set_tag_bucket(self, tag_name):

        bucket_list = [bucket for bucket in self.buckets if bucket["tag_name"] == tag_name]

        if len(bucket_list) == 0:
            bucket = {
                "tag_name": tag_name,
                "data": pd.DataFrame([0 for _ in range(self.window_size)]),
                "ewma": 0.0,
                "ewmvar": 0.0
            }
            self.buckets.append(bucket)
        else:
            bucket = bucket_list[0]
        
        return bucket

    def _get_relative_frequency(self, tag_frequency):
        return tag_frequency / self.cumulative_tag_count

    def _get_significance(self, mean, std, relative_frequency):
        return (relative_frequency - max(self.bias, mean)) / (std + self.bias)

    def _is_significant(self, significance):
        return significance > self.significance_threshold