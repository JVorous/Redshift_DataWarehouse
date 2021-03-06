import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

def load_staging_tables(cur, conn):
    """
    Description: Copies in data from the S3 into the staging tables tables based on the imported
    list 'insert_table_queries'

    Arguments:
        cur: the cursor object.
        conn: the connection object

    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Description: Inserts cleaned rows into final start schema tables based on the imported
    list 'insert_table_queries'

    Arguments:
        cur: the cursor object.
        conn: the connection object

    Returns:
        None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
    Description: Driver function. It establishes the connection and then calls
    the load and insert functions to stage the raw data and ETL it into the final tables

    Arguments:
        None

    Returns:
        None
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
