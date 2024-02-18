import logging
logger = logging.getLogger(__name__)

import time
import json

import marshmallow as m

from keyrock_psql import psql

from .telemetry import Telemetry


class PostgresTelemetry(Telemetry):
    class ConfigSchema(Telemetry.ConfigSchema):
        class Meta:
            include = {
                # @todo: full connection config
                'table_name': m.fields.String(missing='sim_event'),
            }

    def load_config(self, config):
        super().load_config(config)
        self.table_name = config['table_name'].lower()
        self.buffer = []
        self.conn = None

    def __del__(self):
        if len(self.buffer) > 0:
            raise Exception('event buffer not empty (was telemetry shut down?)')

    def get_conn(self):
        if self.conn is None:
            self.conn = psql.Connection({
            	'host': 'pg',
                'port': 5432,
                'db': 'telemetry_test',
                'user': 'postgres',
                'pass': 'postgres',
            })
        return self.conn

    def close_conn(self):
        if self.conn is not None:
            self.conn.disconnect()
            self.conn = None

    def shutdown(self):
        self.send_buffer()
        super().shutdown()

    def record_event(self, event_name, event_data):
        self.buffer.append({
            "event_name": event_name,
            "event_data": event_data,
        })
        return True

    def send_buffer(self):
        conn = self.get_conn()
        logger.debug('@TODO: PostgresTelemetry: send_buffer')
        #write_pandas(conn, df, self.table_name)
        self.close_conn()
        self.buffer = []
