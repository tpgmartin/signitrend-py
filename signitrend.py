class SigniTrend():

    def __init__(self, bias: float = 1.0, significance_threshold: float = 6.0):
        self.bias = bias
        self.significance_threshold = significance_threshold
        self.frequency_map = dict()
        self.stats_map = dict()
    
    def index_new_tags(self, tags: list):
        refinement = []
        unique_tags = set(tags)

        for tag in unique_tags:
            frequency = frequency_map.get(tag, 0)
            self.frequency_map[tag] = frequency + 1
            
            # need to handle case of updating in subsequent time units
            mean, std = 0.0, 0.0
            # get statistics
            if tag in self.stats_map:
                mean, std = self.stats_map[tag]

            frequency = self.frequency_map[tag]
            significance = self._calculate_get_significance(mean, std, frequency)

            if self._is_frequency_significant(significance):
                refinement.append((tag, significance)))
        
        if refinement:
            return refinement
    
    def _is_frequency_significant(self, significance):
        return significance > self.significance_threshold

    def _get_significance(self, mean, std, frequency):
        return (frequency - max(self.beta, mu)) / (sigma + self.beta)
