from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import task, dag

from datetime import datetime, timedelta
from typing import Dict

# returning unique values
# @task.python # PythonOperator
# def extract(): # you can now remove the underscore because the function name becomes the id due to the decorator
#     partner_name = 'netflix'
#     partner_path = '/partners/netflix'
#     return partner_name

# to return multiple values there are slightly differences
# @task.python(task_id='extract_partners', do_xcom_push=False) # do_xcom_push avoids the 'return_value'
# def extract() -> Dict[str, str]: # alternatively to multiple_outputs you can type the outputs
@task.python(task_id='extract_partners', do_xcom_push=False, multiple_outputs=True) # this puts values into different xcoms
def extract(): # you can now remove the underscore because the function name becomes the id due to the decorator
    partner_name = 'netflix'
    partner_path = '/partners/netflix'
    return {'partner_name': partner_name, 'partner_path': partner_path}

@task.python
def process(partner_name, partner_path):
    print(partner_name, partner_path)

with DAG(
    dag_id='decorators',
    description='DAG in charge of processing customer data with XCOM',
    start_date=datetime(2021, 1, 1),
    schedule_interval='@daily',
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'],
    catchup=False, 
    max_active_runs=1,
    ) as dag: 
    # process(extract()) # establishing the dependencies using decorators
    settings = extract()
    process(settings['partner_name'], settings['partner_path'])


# This decorator is not working :(
# @dag(
#     description='DAG in charge of processing customer data with XCOM',
#     start_date=datetime(2021, 1, 1),
#     schedule_interval='@daily',
#     dagrun_timeout=timedelta(minutes=10),
#     tags=['data_science', 'customers'],
#     catchup=False, 
#     max_active_runs=1,)
# def decorators():
#     process(extract()) # establishing the dependencies using decorators

# decorators()