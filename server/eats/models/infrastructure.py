class Infrastructure:

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def get_admin_name (self):
        return self.get_names(self.eats_topic_map.admin_name_type)[0].get_value()

    def set_admin_name (self, name):
        if name == self.get_admin_name():
            return
        try:
            self._default_manager.get_by_admin_name(name)
            # QAZ: Raise a specific exception with error message.
            raise Exception
        except self.DoesNotExist:
            pass
        self.get_names(self.eats_topic_map.admin_name_type)[0].set_value(name)

    def __str__ (self):
        return self.get_admin_name()
