from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from datetime import datetime, timedelta

# PostgresOperator by default only accepts sql templates; by creating a new class that inherits the previous one we are able to template the parameter "parameters"; this allows us to custom different operators to accept jinja syntax
class CustomPostgresOperator(PostgresOperator):
    template_fields = ('sql', 'parameters')

def _extract(partner_name):
    print(partner_name)

with DAG(
    dag_id='my_dag',
    description='DAG in charge of processing customer data',
    start_date=datetime(2021, 1, 1), # each task can have diff dates
    schedule_interval='@daily', # frequency of you dag being triggered (see docs)
    dagrun_timeout=timedelta(minutes=10),
    tags=['data_science', 'customers'], # filter dags on ui, e.g. data science, data engineer
    catchup=False, # prevent to do not run several tasks simuntaneously
    max_active_runs=1, # you wont have more than 1 dag run, usefull when you have dependecies between dags
    ) as dag: # unique id accross all dags
    
    extract = PythonOperator(
        task_id='extract',
        python_callable=_extract,
        op_args=['{{ var.json.my_dag_partner.name }}']
    )
    fetching_data = CustomPostgresOperator(
        task_id='fetching_data',
        sql='sql/MY_REQUEST.sql', # see registry.astronomer.io; ds =  current data from jinja template; a good practice is to create a sql file here
        parameters={
            'next_ds': '{{ next_ds }}',
            'previous_ds': '{{ prev_ds }}',
            'partner_name': '{{ var.json.my_dag_partner.name }}'
        }, # thanks to custom operator we are able to inject data at runtime; this parameters is now templated
    )