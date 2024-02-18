import time
import json

try:
    import pandas as pd
    import snowflake.connector as snow
    from snowflake.connector.pandas_tools import write_pandas
except:
    pd = None
    snow = None
    write_pandas = None

import marshmallow as m
import logging
logger = logging.getLogger(__name__)

from .telemetry import Telemetry


snowflake_logger = logging.getLogger('snowflake')
snowflake_logger.setLevel(logging.INFO)


class SnowflakeTelemetry(Telemetry):
    class ConfigSchema(Telemetry.ConfigSchema):
        class Meta:
            include = {
                'debug': m.fields.Boolean(missing=False),
                'table_name': m.fields.String(missing='sim_event'),
            }

    def load_config(self, config):
        super().load_config(config)
        self.debug = config['debug']
        self.table_name = config['table_name'].upper()
        self.buffer = []
        self.conn = None

    def __del__(self):
        if snow is None:
            return

        if len(self.buffer) > 0:
            raise Exception('event buffer not empty (was telemetry shut down?)')

    def get_conn(self):
        if snow is None:
            return None

        # TODO: Clean this up
        if self.debug:
            self.conn = None
        elif self.conn is None:
            self.conn = snow.connect(user="[USER]",
               numpy=True,
               password="[PASSWORD]",
               account="[ACCOUNT]",
               warehouse="COMPUTE_WH",
               database="[DATABASE]",
               schema="PUBLIC")
        return self.conn

    def close_conn(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def shutdown(self):
        self.send_buffer()
        super().shutdown()

    def record_event(self, event_name, event_data):
        if self.needs_data():
            self.buffer.append({
                "EVENT_NAME": event_name,
                "EVENT_DATA": event_data,
            })
        # TODO: If not throttled
        return True

    def send_buffer(self):
        if pd is None:
            return None

        df = pd.DataFrame.from_records(self.buffer)
        if self.debug:
            logger.debug('send_buffer:')
            logger.debug(json.dumps(self.buffer, indent=2))
        elif self.needs_data():
            conn = self.get_conn()
            write_pandas(conn, df, self.table_name)
            self.close_conn()
        self.buffer = []

    def create_cond_str(self, dict_val):
        str_array = []
        for key, val in dict_val.items():
            str_array.append("event_data:{0}::string='{1}'".format(key, val))
        cond_str = " AND ".join(str_array)
        return cond_str

    def clear_extra_data(self, uq_dict):
        if uq_dict is None:
            return

        pos_str = self.create_cond_str(uq_dict['discard'])
        neg_str = self.create_cond_str(uq_dict['keep'])

        cmd = ("DELETE FROM {table_name}"
               " WHERE ({pos_str})"
               " AND NOT ({neg_str})").format(
                table_name=self.table_name,
                pos_str=pos_str,
                neg_str=neg_str)
        logger.debug(cmd)

        conn = self.get_conn()
        if conn:
           conn.cursor().execute(cmd)
        self.close_conn()

    def has_prior_data(self, uq_dict):
        # Need to record whether this has prior data,
        # and not record again if so
        has_sim_result = False

        if uq_dict is None:
            return has_sim_result

        pos_str = self.create_cond_str(uq_dict['keep'])
 
        query = (
            "SELECT COUNT(1) AS result_count"
            " FROM {table_name}"
            " WHERE event_name='sim_complete'"
            " AND ({pos_str})"
            ).format(table_name=self.table_name, pos_str=pos_str)
        logger.debug(query)

        conn = self.get_conn()
        if conn:
            result_count = conn.cursor().execute(query).fetchone()
            logger.debug('result count: {}'.format(str(result_count)))
            has_sim_result = int(result_count[0]) > 0
        self.close_conn()

        return has_sim_result
