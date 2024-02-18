import json
import logging
logger = logging.getLogger(__name__)

from .telemetry import Telemetry

class LoggingTelemetry(Telemetry):
    def record_event(self, event_name, event_data):
        logger.debug('{}: {}'.format(event_name, json.dumps(event_data, indent=2)))

        # TODO: If not throttled
        return True