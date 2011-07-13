class Infrastructure (object):

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def get_admin_name (self):
        return self.get_names(self.eats_topic_map.admin_name_type)[0].get_value()

    def set_admin_name (self, name):
        self.get_names(self.eats_topic_map.admin_name_type)[0].set_value(name)
        
    def topic_exists (self):
        return False
