from dagster import asset, Output, String, AssetIn, FreshnessPolicy, MetadataValue
from dagster_mlflow import mlflow_tracking
# %%
import pandas as pd

import psycopg2
import pandas as pd
import os

from dagster_dbt import get_asset_key_for_model
from dagster import AssetKey

def read_table(schema_name, table_name):

    # Get PostgreSQL connection parameters from environment variables
    dbname = os.environ.get('PG_DBNAME')
    user = os.environ.get('POSTGRES_USER')
    password = os.environ.get('POSTGRES_PASSWORD')
    host = os.environ.get('PG_HOST')
    port = os.environ.get('PG_PORT')

    # Establish a connection to the PostgreSQL database
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    # Create a cursor object to interact with the database
    cursor = connection.cursor()
    sql_query = f'SELECT * FROM {schema_name}.{table_name}'
    # Execute the query
    cursor.execute(sql_query)
    # Fetch all rows from the result set
    rows = cursor.fetchall()
    # Get the column names from the cursor description
    columns = [desc[0] for desc in cursor.description]
    # Create a Pandas DataFrame using the fetched data and column names
    df = pd.DataFrame(rows, columns=columns)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return df




@asset(
        deps=["scores_movies_users"],       #Testeado ok.
)
def training_data() -> Output[pd.DataFrame]:   
    result = read_table(schema_name="target", table_name="scores_movies_users")
    return Output(
        result,
        metadata={
            "Total rows": len(result),
        },
    )
    
