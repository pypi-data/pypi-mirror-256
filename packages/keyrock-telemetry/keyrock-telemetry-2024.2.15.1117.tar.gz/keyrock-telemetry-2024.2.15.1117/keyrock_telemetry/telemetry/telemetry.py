import marshmallow as m
import logging
logger = logging.getLogger(__name__)

from keyrock_hcs import hcs


class Telemetry(hcs.HCSObject):
    class ConfigSchema(hcs.HCSObject.ConfigSchema):
        class Meta:
            include = {
            }

    def load_config(self, config):
        super().load_config(config)
        self._needs_data = None

    def init(self, uq_dict=None):
        self.clear_extra_data(uq_dict)
        self._needs_data = not self.has_prior_data(uq_dict)

    def needs_data(self):
        return self._needs_data

    def clear_extra_data(self, uq_dict):
        pass

    def has_prior_data(self, uq_dict):
        return False

    def record_event(self, event_name, event_data):
        raise NotImplementedError()

    def shutdown(self):
        pass
