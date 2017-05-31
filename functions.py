import psycopg2


def import_config():
    """Get the credentials for database access"""
    with open("config.txt") as config:
        config = config.readlines()
    return config


def database_query(query):
    config = import_config()
    try:
        connect_str = "dbname={} user={} host='localhost' password={}".format(config[0], config[0], config[1])
        conn = psycopg2.connect(connect_str)
        with conn:
            with conn.cursor() as cur:
                cur.execute(query)
                query_result = cur.fetchall()
        return query_result
    except:
        print("The database cannot be accessed")

