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

    # df columns: tag, creation_year_month, tag_count, all_tags_count
    # creation_year_month should be in chronological order
    # this is just to initialise representation of tags
    def index_tag(self, tag_row):

        tag = tag_row["tag"]
        frequency = self.frequency_map.get(tag, 0)
        self.frequency_map[tag] = frequency + tag_row["tag_count"]
        self.cumulative_tag_count += tag_row["all_tags_count"]

        # TODO:
        # * need to check initialisation conditions
        # * need to handle case of updating in subsequent time units
        mean, std = 0.0, 0.0
        if tag in self.stats_map:
            mean, std = self.stats_map[tag]
        
        relative_frequency = self._get_relative_frequency(self.frequency_map[tag])
        significance = self._get_significance(mean, std, relative_frequency)

        if self._is_significant(significance):
            return (tag, significance)

    def _get_relative_frequency(self, tag_frequency):
        return tag_frequency / self.cumulative_tag_count

    def _get_significance(self, mean, std, relative_frequency):
        return (relative_frequency - max(self.bias, mean)) / (std + self.bias)

    def _is_significant(self, significance):
        return significance > self.significance_threshold