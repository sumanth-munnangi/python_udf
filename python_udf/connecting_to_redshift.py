import redshift_connector as rc
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Using sql_alchemy
db_pass = 'password'
quoted_pass = quote_plus(db_pass)
connection_string = f"postgresql://'user_name':{quoted_pass}@'redshift_cluster_link':'port - 5439'/'db_name'"

try:
    engine = create_engine(connection_string)
except:
    print("Please check your RedShift credentials")

# using redshift_connector update the credentials


conn = rc.connect(
    host='redshift_cluster_link',
    port='port - 5439',
    database='db_name',
    password='password',
    user='user_name')
conn.autocommit = True

cursor = rc.cursor.Cursor(conn, 'format')

# Unload data to S3 from redshift

# Constants

query = """select * from ----"""
path = """s3 path"""
# Unload Command

cursor.execute(f"""unload ($$

{query}

$$) to {path}
iam_role 'arn:aws:iam::--- IAM role'
PARQUET 
CLEANPATH 
MAXFILESIZE 30 MB
PARALLEL ON;""")

# Note to use clean path to delete the path before unloading - if you use ALLOWOVERWRITE it will only overwrite the
# partitions


# Copy data from S3 to Redshift
# make sure to create the table before copying data
# Truncate if you need to overwrite the table
query_write = """copy schema.table_to_be_copied_into 
from 's3 path' 
iam_role 'arn:aws:iam::--- IAM role'
FORMAT AS PARQUET
"""

cursor.execute(query_write)