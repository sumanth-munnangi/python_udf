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

# using redshift_connector


conn = rc.connect(
    host='redshift_cluster_link',
    port='port - 5439',
    database='db_name',
    password='password',
    user='user_name')
conn.autocommit = True

cursor = rc.cursor.Cursor(conn, 'format')
