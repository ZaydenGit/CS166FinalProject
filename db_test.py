#!/usr/bin/env python3
# ----------------------------------------------------------
# Template Python User Interface
# ================================
#
# Database Management Systems
# Department of Computer Science & Engineering
# University of California - Riverside
#
# Target DBMS: 'Postgres'
#
# ----------------------------------------------------------

import sys
import psycopg2
import os


class EmbeddedSQL:
    """
    A simple embedded SQL utility class designed to work with PostgreSQL
    via the psycopg2 driver.
    """

    def __init__(self, dbname, dbport, user, passwd=""):
        """
        Creates a new instance of EmbeddedSQL and establishes a physical
        connection to the database.

        :param dbname:  the name of the database
        :param dbport:  the port the PostgreSQL server is running on
        :param user:    the user name used to login to the database
        :param passwd:  the user login password
        """
        print("Connecting to database...")
        try:
            self._connection = psycopg2.connect(
                database=dbname,
                user=user,
                password=passwd,
                host="localhost",
                port=dbport
            )
            print(f"Connection URL: postgresql://localhost:{dbport}/{dbname}\n")
            print("Done")
        except Exception as e:
            print(f"Error - Unable to Connect to Database: {e}", file=sys.stderr)
            print("Make sure you started postgres on this machine")
            sys.exit(-1)

    def run_sql(self, sql, params=None):
        cursor = self._connection.cursor()
        cursor.execute(sql, params)
        
        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        res = []
        res.append("\t".join(col_names))

        for row in rows:
            res.append("\t".join(str(val) for val in row))
        # Print header
        cursor.close()
        return "\n".join(res)

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
        :return:       the number of rows returned
        """
        cursor = self._connection.cursor()
        cursor.execute(query, params)

        col_names = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        row_count = 0

        # Print header
        print("\t".join(col_names))

        # Print each row
        for row in rows:
            print("\t".join(str(val) for val in row))
            row_count += 1

        cursor.close()
        return row_count

    def cleanup(self):
        """
        Closes the physical connection if it is open.
        """
        try:
            if self._connection is not None:
                self._connection.close()
        except Exception:
            pass  # ignored


# ----------------------------------------------------------
# Main
# ----------------------------------------------------------

def main():
    # if len(sys.argv) != 4:
    #     print(
    #         f"Usage: python {sys.argv[0]} <dbname> <port> <user>",
    #         file=sys.stderr
    #     )
    #     return


    # dbname = sys.argv[1]
    # dbport = sys.argv[2]
    # user   = sys.argv[3]

    user = os.environ.get('USER') #https://docs.python.org/3/library/os.html#os.environ
    dbport = os.environ.get('PGPORT') 
    if not user:
        print ("User not set")
        return
    if not dbport:
        print ("Port not set")
        return
    dbname = f"{user}_finalproj_DB"

    esql = None
    try:
        esql = EmbeddedSQL(dbname, dbport, user, "")

        print ("\nTesting database query...")
        esql.execute_query("SELECT version()")
    except Exception as e:
        print(e, file=sys.stderr)
    finally:
        if esql is not None:
            print("Disconnecting from database...", end="")
            esql.cleanup()
            print("Done\n\nBye!")


if __name__ == "__main__":
    main()
