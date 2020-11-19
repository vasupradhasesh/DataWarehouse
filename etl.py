import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
"""
Description: This function can be used to copy(load) staging events
and staging songs into the S3 bucket from redshift

Arguments:
    cur: the cursor object. 
    conn: the connection object. 

Returns:
    None
"""    
    for query in copy_table_queries:
        print(query)
        cur.execute(query)
        print("Loaded")
        conn.commit()


def insert_tables(cur, conn):
"""
Description: This function can be used to insert
tables created.

Arguments:
    cur: the cursor object. 
    conn: the connection object. 

Returns:
    None
"""
    for query in insert_table_queries:
        cur.execute(query)
        print("Inserted")
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')
    
    print('Establishing connection')
    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    print('Connection established')
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()
    print("Ended successfully")


if __name__ == "__main__":
    main()