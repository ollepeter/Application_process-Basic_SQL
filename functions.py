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
            with conn.cursor() as cursor:
                cursor.execute(query)
                query_result = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]
                query_result.insert(0, column_names)
        return query_result
    except:
        print("The database cannot be accessed")

