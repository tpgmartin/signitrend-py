class SigniTrend():

    def __init__(self, bias: float = 1.0, significance_threshold: float = 6.0):
        self.bias = bias
        self.frequency_map = dict()
        self.significance_threshold = significance_threshold
        self.stats_map = dict()
        self.total_tag_count = 0
        self.trending_tags = []
    
    def index_new_tag(self, tag: string):

        self.total_tag_count += 1

        frequency = frequency_map.get(tag, 0)
        self.frequency_map[tag] = frequency + 1
        
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

    def end_of_day_analysis(self):

        for tag in self.frequency_map:
            mu, std = self.stats_map[tag]
            relative_frequency = self._get_relative_frequency(self.frequency_map[tag])
            significance = self._get_significance(mean, std, relative_frequency)

            if self._is_significant(significance):
                self.trending_tags.append(tag, significance)

        return self.trending_tags
    
    def _get_relative_frequency(self, frequency):
        return frequency / self.total_tag_count

    def _get_significance(self, mean, std, frequency):
        return (frequency - max(self.beta, mu)) / (sigma + self.beta)

    def _is_significant(self, significance):
        return significance > self.significance_threshold