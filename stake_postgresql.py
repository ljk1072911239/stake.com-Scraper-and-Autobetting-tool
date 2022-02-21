import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

POSTGRES_USERNAME = 'postgres'
POSTGRES_PASSWORD = 'asd'
POSTGRES_IP = 'localhost'
POSTGRES_PORT = '5432'
POSTGRES_DB_NAME = 'stake_data'
POSTGRES_SCHEMA_NAME = 'public'

DATABASE_URL = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_IP}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}'

ENGINE = create_engine(DATABASE_URL)


def set_table(dataframe: pd.DataFrame, table):
    """
    Function to upload dataframe to database as a given table
    Drop the table first if it exists, then create a new one and load the data!
    """
    global ENGINE
    global POSTGRES_SCHEMA_NAME

    # First, clear the given table
    try:
        with ENGINE.connect() as con:
            # statement = f"""DELETE FROM public.{table}""" || Use this if you want to delete the existing table.
            statement = f"""DROP TABLE IF EXISTS public.{table}"""
            con.execute(statement)
    except Exception as e:
        print("Exception happened when deleting from the table")
        print(e)

    dataframe.to_sql(table, ENGINE, schema=POSTGRES_SCHEMA_NAME, if_exists='append',
                     index=False)


def get_table(table):
    global ENGINE

    dataframe: pd.DataFrame = pd.read_sql(f"SELECT * FROM {POSTGRES_SCHEMA_NAME}.{table}", ENGINE)

    return dataframe


if __name__ == "__main__":

    """ If you run the script individually, it will create the database! """

    if not database_exists(DATABASE_URL):
        create_database(DATABASE_URL)
