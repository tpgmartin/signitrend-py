class SigniTrend():

    def __init__(self, bias: float = 1.0, significance_threshold: float = 6.0, window_size: int = 12):
        self.bias = bias
        self.buckets = []
        self.frequency_map = dict()
        self.significance_threshold = significance_threshold
        self.stats_map = dict()
        self.time_step = 1
        self.total_tag_count = 0
        self.trending_tags = []
        self.window_size = window_size

    # df columns: tag, creation_year_month, tag_count, all_tags_count
    def add_new_tag_timestep(self, tag: dict):
        tag = 
        frequency = frequency_map.get(tag, 0)


    # WIP
    def index_new_tag(self, tag: str):
        # only read from buckets here

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

    def next_time_step(self):
        # 1. Create new list "update_table" - this is a hash table
        # 2. For each tag in frequency map, if tag not in update_table or if 
        # frequency is greater then update "update_table"
        # 3. For each non "None" entry in update_table, update bucket by 
        # calling "self._update_bucket"
        update_table = []

        for tag in self.frequency_map:
            frequency = self.frequency_map[tag]
            tag_dict = [element for element in update_table if element["tag"] == tag]
            if len(tag_dict) == 0:
                update_table.append({
                    "tag": tag,
                    "frequency": frequency
                })
            # this might not be necessary
            elif tag_dict[0]["frequency"] < frequency:
                tag_dict[0]["frequency"] = frequency

        for tag in update_table:
            self._update_bucket(tag)

        self.time_step += 1
        self.trending_tags = []

    def end_of_day_analysis(self):

        for tag in self.frequency_map:
            mean, std = self.stats_map[tag]
            relative_frequency = self._get_relative_frequency(self.frequency_map[tag])
            significance = self._get_significance(mean, std, relative_frequency)

            if self._is_significant(significance):
                self.trending_tags.append(tag, significance)

        return self.trending_tags
    
    def _get_relative_frequency(self, frequency):
        return frequency / self.total_tag_count

    def _get_significance(self, mean, std, frequency):
        return (frequency - max(self.beta, mean)) / (std + self.beta)

    def _is_significant(self, significance):
        return significance > self.significance_threshold

    def _update_bucket(self, tag: dict):
        # tag = {tag: "tagName", frequency: 123}
        bucket = [bucket for bucket in self.buckets if bucket["tag"] == tag["tag"]]
        # For given tag bucket
        # relative_frequency = self._get_relative_frequency(tag["frequency"])
        # Recalculate EWM for window for updated bucket
        # Recalculate ewma and ewmvar
