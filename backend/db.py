import sys
import psycopg2
import os


class EmbeddedSQL:
    """
    A simple embedded SQL utility class designed to work with PostgreSQL
    via the psycopg2 driver.
    """

    def __init__(self):
        """
        Creates a new instance of EmbeddedSQL and establishes a physical
        connection to the database.

        :param dbname:  the name of the database
        :param dbport:  the port the PostgreSQL server is running on
        :param user:    the user name used to login to the database
        :param passwd:  the user login password
        """
        print("Connecting to database...")

        user = os.environ.get("USER")
        dbport = os.environ.get("PGPORT")

        assert user is not None, "User environment variable not set"
        assert dbport is not None, "PGPORT environment variable not set"

        dbname = f"{user}_finalproj_DB"

        try:
            self._connection = psycopg2.connect(
                database=dbname,
                user=user,
                host="localhost",
                port=dbport
            )
            print(f"Connection URL: postgresql://localhost:{dbport}/{dbname}\n")
            print("Done")
        except Exception as e:
            print(f"Error - Unable to Connect to Database: {e}", file=sys.stderr)
            print("Make sure you started postgres on this machine")
            sys.exit(-1)

    def execute_update(self, sql):
        """
        Executes an update SQL statement (CREATE, INSERT, UPDATE, DELETE, DROP).

        :param sql: the input SQL string
        """
        cursor = self._connection.cursor()
        cursor.execute(sql)
        self._connection.commit()
        cursor.close()

    def execute_query(self, query, params=None):
        """
        Executes a SELECT query and prints the results to standard output.

        :param query:  the input query string
        :param params: optional tuple of parameters for parameterized queries
        :return:       column names and rows
        """
        cursor = self._connection.cursor()
        cursor.execute(query, params)

        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        # row_count = 0

        # # Print header
        # print("\t".join(col_names))

        # # Print each row
        # for row in rows:
        #     print("\t".join(str(val) for val in row))
        #     row_count += 1

        cursor.close()
        return col_names, rows

    def cleanup(self):
        """
        Closes the physical connection if it is open.
        """
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception:
            pass  # ignored