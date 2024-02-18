from keyrock_hcs import hcs

from .telemetry import Telemetry
from .snowflake import SnowflakeTelemetry
from .postgres import PostgresTelemetry
from .logging import LoggingTelemetry

type_map = {
    'logging': LoggingTelemetry,
    'snowflake': SnowflakeTelemetry,
    'postgres': PostgresTelemetry,
}

factory = hcs.TypeConfigFactory(type_map)
