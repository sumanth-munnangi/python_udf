import time
import pprint
import datetime as dt

import pandas as pd
import numpy as np

import boto3

# UDF to run an athena Query using Boto3

def run_query(query, database, s3_output):
    client = boto3.client('athena', region_name='ap-south-1' )
    response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': s3_output,}
        )
    print('Execution ID: ' + response['QueryExecutionId'])
    return response

# UDF to check the status of the query
def check_query_status(query_id):
    client = boto3.client('athena', region_name='ap-south-1' )
    response = client.get_query_execution(
        QueryExecutionId = query_id)
    return response

# Run the Queries

for q in queries:
    print("Executing query: %s" % (q))
    res = run_query(q, database, s3_output)
    query_id = res['QueryExecutionId']
    time.sleep(5)
    status = check_query_status(query_id)
    status = status['QueryExecution']['Status']['State']
    print(f'Query Status is {status} \n')

# Check the status
timeout_start = time.time()

while time.time() < timeout_start + timeout:
    status = check_query_status(query_id)
    if status['QueryExecution']['Status']['State'] == 'FAILED':
        print('Query Failed')
        path = None
        break
    if status['QueryExecution']['Status']['State'] == 'SUCCEEDED':
        path = 's3://datascience-analysis-athena/athenaqueryresult/' + str(query_id) + '.csv'
        print(f"Merging Completed and Path of file saved is : {path}\n")
        break