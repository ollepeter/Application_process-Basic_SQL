import psycopg2


def import_config():
    """Get the credentials for database access"""
    with open("config.txt") as config:
        config = config.readlines()
    return config
