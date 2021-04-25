from types import MethodType
from django.test.runner import DiscoverRunner
from django.db import connections

"""
    Grant privileges to test database schemas
"""

def prepare_database(self):
    self.connect()
    self.connection.cursor().execute("""
    CREATE SCHEMA bp_app AUTHORIZATION postgres;
    GRANT ALL ON SCHEMA bp_app TO postgres;
    CREATE SCHEMA schema_2 AUTHORIZATION postgres;
    GRANT ALL ON SCHEMA schema_2 TO postgres;
    CREATE SCHEMA schema_3 AUTHORIZATION postgres;
    GRANT ALL ON SCHEMA schema_3 TO postgres;
    ALTER ROLE postgres SET search_path TO bp_app;
    """)


class TestRunner(DiscoverRunner):

    def setup_databases(self, **kwargs):
        for connection_name in connections:
            connection = connections[connection_name]
            connection.prepare_database = MethodType(prepare_database, connection)
        return super().setup_databases(**kwargs)
