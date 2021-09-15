import time
from airflow import DAG
from airflow.decorators import task, dag
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.external_task import ExternalTaskSensor

from groups.process_tasks import process_tasks
from datetime import datetime, timedelta

partners = {
    'partner_snowflake': {
        'name': 'snowflake',
        'path': '/partners/snowflake',
        'priority': 2,
        'pool': 'snowflake'
    },
    
    'partner_netflix': {
        'name': 'netflix',
        'path': '/partners/netflix',
        'priority': 3,
        'pool': 'netflix',
    },
    
    'partner_astronomer': {
        'name': 'astronomer',
        'path': '/partners/astronomer',
        'priority': 1,
        'pool': 'astronomer'
    },
    
}

default_args = {
    'owner': 'airflow',
    'start_date':datetime(2021, 1, 1),
}

with DAG(
    dag_id='cleaning_dag',
    default_args=default_args,
    schedule_interval='@daily', catchup=False
) as dag:
    waiting_for_task = ExternalTaskSensor(
        task_id='waiting_for_task',
        external_dag_id='branching',
        external_task_id='storing',
        failed_states=['failed', 'skipped'],
        allowed_states=['success'],
    )

    cleaning_xcoms = PostgresOperator(
        task_id='cleaning_xcoms',
        sql='sql/CLEANING_XCOMS.sql',
        postgres_conn_id='postgres'
    )

    waiting_for_task >> cleaning_xcoms