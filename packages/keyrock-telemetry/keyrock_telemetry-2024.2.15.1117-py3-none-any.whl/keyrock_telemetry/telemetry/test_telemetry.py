import unittest

try:
    import psycopg2
except:
    psycopg2 = None

try:
    import snowflake
except:
    snowflake = None

from keyrock_psql import psql

from . import *

import logging
logger = logging.getLogger(__name__)
logging.getLogger('keyrock_telemetry.telemetry.logging').setLevel(logging.INFO)


class LoggingTest(unittest.TestCase):
    def test_event(self):
        api = LoggingTelemetry()
        api.init()
        success = api.record_event('test_event', {'x': 69, 'type': 'logging'})
        self.assertEqual(success, True)
 
 
class SnowflakeTest(unittest.TestCase):
    @classmethod
    def setupClass(cls):
        if snowflake is None:
            raise unittest.SkipTest('snowflake not installed')

    def test_event(self):
        api = SnowflakeTelemetry({'debug': True, 'table_name': 'test'})
        api.init()
        for x in range(0, 3):
            api.record_event('long_test_event_name_{}'.format(x), {'x': x, 'type': 'snowflake'})
        api.shutdown()
        # TODO: Check that three events are in the buffer
        self.assertEqual(1, 1)


class PostgresTest(unittest.TestCase):
    config = {
        'host': 'pg',
        'port': 5432,
        'db': 'telemetry_test',
        'user': 'postgres',
        'pass': 'postgres',
    }

    @classmethod
    def setUpClass(cls):
        if psycopg2 is None:
            raise unittest.SkipTest('psycopg2 not installed')

        psql.wait_for_server(cls.config, timeout_sec=15)

        try:
            assert (not psql.database_exists(cls.config)), 'database already exists'
            psql.create_database(cls.config)
        except Exception as e:
            cls.tearDownClass()
            raise e

    @classmethod
    def tearDownClass(cls):
        assert (psql.database_exists(cls.config)), 'database does not exist'

        # Remove the test database
        psql.drop_database(cls.config)

    def test_event(self):
        api = PostgresTelemetry()
        api.init()
        success = api.record_event('test_event', {'x': 69, 'type': 'postgres'})
        api.shutdown()
        self.assertEqual(success, True)
