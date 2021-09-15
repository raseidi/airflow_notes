from airflow import DAG
from airflow.decorators import task
from datetime import datetime

def generate_dag(dag_id, schedule_interval, details, default_args):
    with DAG(dag_id, schedule_interval=schedule_interval, default_args=default_args) as dag:
        @task.python
        def process(path):
            print(f'Processing: {path}')
            
        process(details['path'])

    return dag