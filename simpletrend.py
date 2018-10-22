import pandas as pd

class SimpleTrend():

    def __init__(self, bias: float = 1.0, significance_threshold: float = 6.0, window_size: int = 12):
        self.bias = bias
        self.buckets = []
        self.frequency_map = dict()
        self.significance_threshold = significance_threshold
        self.stats_map = dict()
        self.cumulative_tag_count = 0
        self.trending_tags = []
        self.window_size = window_size

    # df columns: tag_name, creation_year_month, tag_count, all_tags_count
    # creation_year_month should be in chronological order
    # this is just to initialise representation of tags
    def index_tag(self, tag_row):

        tag_name = tag_row["tag_name"]
        frequency = self.frequency_map.get(tag_name, 0)
        self.frequency_map[tag_name] = frequency + tag_row["tag_count"]
        self.cumulative_tag_count += tag_row["all_tags_count"]

        # might only need to create a new bucket rather than return as well
        bucket = self._get_or_set_tag_bucket(tag_name)

        # TODO:
        # * need to check initialisation conditions
        # * need to handle case of updating in subsequent time units
        mean, std = 0.0, 0.0
        if tag_name in self.stats_map:
            mean, std = self.stats_map[tag_name]
        
        relative_frequency = self._get_relative_frequency(self.frequency_map[tag_name])
        significance = self._get_significance(mean, std, relative_frequency)

        if self._is_significant(significance):
            return (tag_name, significance)
    
    # def next_timestep(self):

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